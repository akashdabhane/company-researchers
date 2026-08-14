import json
import os
import uuid
import datetime
from typing import Dict, List, Optional, Any
from app.database.database import SessionLocal, engine, Base
from app.database.models import ChatSessionModel, ChatMessageModel

class PostgresChatStore:
    def __init__(self):
        self.init_db()

    def init_db(self):
        try:
            Base.metadata.create_all(bind=engine)
            print("[DATABASE] PostgreSQL tables created/verified successfully.")
            self.migrate_legacy_json_if_needed()
        except Exception as e:
            print(f"[DATABASE WARNING] Could not auto-create PostgreSQL tables: {e}")

    def migrate_legacy_json_if_needed(self):
        """Migrate any existing chat_history.json file entries into PostgreSQL on startup."""
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "chat_history.json")
        if not os.path.exists(json_path):
            return

        db = SessionLocal()
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            if not loaded or not isinstance(loaded, dict):
                return

            print("[DATABASE] Migrating legacy chat_history.json to PostgreSQL...")
            
            # Normalize user dicts
            user_dicts = loaded
            sample = next(iter(loaded.values()), None)
            if sample and "thread_id" in sample:
                user_dicts = {"anonymous": loaded}

            for user_id, threads in user_dicts.items():
                for thread_id, chat in threads.items():
                    existing = db.query(ChatSessionModel).filter_by(thread_id=thread_id).first()
                    if not existing:
                        session_model = ChatSessionModel(
                            thread_id=thread_id,
                            user_id=user_id,
                            company_name=chat.get("company_name", "Migrated Research"),
                            website_url=chat.get("website_url", ""),
                            research_data=chat.get("research_data", {}),
                        )
                        db.add(session_model)
                        db.commit()

                        # Add messages
                        for m in chat.get("messages", []):
                            msg_model = ChatMessageModel(
                                id=m.get("id") or str(uuid.uuid4()),
                                thread_id=thread_id,
                                user_id=user_id,
                                role=m.get("role", "assistant"),
                                type=m.get("type", "text"),
                                content=m.get("content", ""),
                            )
                            db.add(msg_model)
                        db.commit()

            print("[DATABASE] Legacy chat_history.json migration completed successfully.")
            # Rename legacy file after migration
            os.rename(json_path, json_path + ".migrated_bak")

        except Exception as e:
            print(f"[DATABASE WARNING] Migration of legacy JSON failed: {e}")
            db.rollback()
        finally:
            db.close()

    def get_all_chats(self, user_id: str = "anonymous") -> List[Dict[str, Any]]:
        db = SessionLocal()
        try:
            sessions = (
                db.query(ChatSessionModel)
                .filter(ChatSessionModel.user_id == user_id)
                .order_by(ChatSessionModel.updated_at.desc())
                .all()
            )

            result = []
            for s in sessions:
                msg_count = db.query(ChatMessageModel).filter_by(thread_id=s.thread_id).count()
                result.append({
                    "thread_id": s.thread_id,
                    "company_name": s.company_name,
                    "website_url": s.website_url,
                    "title": f"Research: {s.company_name}",
                    "created_at": s.created_at.isoformat() if s.created_at else "",
                    "updated_at": s.updated_at.isoformat() if s.updated_at else "",
                    "message_count": msg_count,
                })
            return result
        except Exception as e:
            print(f"[DATABASE ERROR] get_all_chats: {e}")
            return []
        finally:
            db.close()

    def get_chat(self, user_id: str, thread_id: str) -> Optional[Dict[str, Any]]:
        db = SessionLocal()
        try:
            session = (
                db.query(ChatSessionModel)
                .filter(ChatSessionModel.thread_id == thread_id, ChatSessionModel.user_id == user_id)
                .first()
            )
            if not session:
                return None
            return session.to_detail_dict()
        except Exception as e:
            print(f"[DATABASE ERROR] get_chat: {e}")
            return None
        finally:
            db.close()

    def create_or_update_research_session(
        self,
        user_id: str,
        thread_id: str,
        company_name: str,
        website_url: str,
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            session = db.query(ChatSessionModel).filter_by(thread_id=thread_id).first()
            now = datetime.datetime.utcnow()

            if session:
                session.user_id = user_id
                session.company_name = company_name
                session.website_url = website_url
                session.research_data = research_data
                session.updated_at = now
            else:
                session = ChatSessionModel(
                    thread_id=thread_id,
                    user_id=user_id,
                    company_name=company_name,
                    website_url=website_url,
                    research_data=research_data,
                    created_at=now,
                    updated_at=now,
                )
                db.add(session)
                db.commit()

            # Ensure initial assistant report message if empty
            msg_count = db.query(ChatMessageModel).filter_by(thread_id=thread_id).count()
            if msg_count == 0:
                report_text = research_data.get("report") if isinstance(research_data, dict) else "Research process completed."
                if not report_text:
                    report_text = "Research process completed."
                initial_msg = ChatMessageModel(
                    id=str(uuid.uuid4()),
                    thread_id=thread_id,
                    user_id=user_id,
                    role="assistant",
                    type="research_report",
                    content=report_text,
                    timestamp=now,
                )
                db.add(initial_msg)
                db.commit()

            db.refresh(session)
            return session.to_detail_dict()

        except Exception as e:
            db.rollback()
            print(f"[DATABASE ERROR] create_or_update_research_session: {e}")
            raise e
        finally:
            db.close()

    def add_message(
        self,
        user_id: str,
        thread_id: str,
        role: str,
        content: str,
        msg_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            session = db.query(ChatSessionModel).filter_by(thread_id=thread_id).first()
            if not session:
                raise ValueError(f"Chat thread {thread_id} not found in database.")

            now = datetime.datetime.utcnow()
            msg = ChatMessageModel(
                id=str(uuid.uuid4()),
                thread_id=thread_id,
                user_id=user_id,
                role=role,
                type=msg_type,
                content=content,
                timestamp=now,
            )
            session.updated_at = now
            db.add(msg)
            db.commit()
            db.refresh(msg)
            return msg.to_dict()

        except Exception as e:
            db.rollback()
            print(f"[DATABASE ERROR] add_message: {e}")
            raise e
        finally:
            db.close()

    def delete_chat(self, user_id: str, thread_id: str) -> bool:
        db = SessionLocal()
        try:
            session = db.query(ChatSessionModel).filter_by(thread_id=thread_id, user_id=user_id).first()
            if session:
                db.delete(session)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"[DATABASE ERROR] delete_chat: {e}")
            return False
        finally:
            db.close()


chat_store = PostgresChatStore()
