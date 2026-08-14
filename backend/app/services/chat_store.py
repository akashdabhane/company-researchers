import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "chat_history.json")

class ChatStore:
    def __init__(self):
        # Structure: { user_id: { thread_id: chat_session } }
        self.chats: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.load_from_disk()

    def load_from_disk(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Support legacy unsegregated store migration
                    if isinstance(loaded, dict):
                        # Check if top-level values are chats or user dicts
                        sample = next(iter(loaded.values()), None)
                        if sample and "thread_id" in sample:
                            self.chats = {"anonymous": loaded}
                        else:
                            self.chats = loaded
        except Exception as e:
            print(f"Error loading chat history from disk: {e}")
            self.chats = {}

    def save_to_disk(self):
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.chats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat history to disk: {e}")

    def get_user_chats(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        if user_id not in self.chats:
            self.chats[user_id] = {}
        return self.chats[user_id]

    def get_all_chats(self, user_id: str = "anonymous") -> List[Dict[str, Any]]:
        user_chats = self.get_user_chats(user_id)
        sorted_chats = sorted(
            user_chats.values(),
            key=lambda x: x.get("updated_at", ""),
            reverse=True
        )
        return [
            {
                "thread_id": c["thread_id"],
                "company_name": c["company_name"],
                "website_url": c["website_url"],
                "title": c.get("title", c["company_name"]),
                "created_at": c["created_at"],
                "updated_at": c["updated_at"],
                "message_count": len(c.get("messages", [])),
            }
            for c in sorted_chats
        ]

    def get_chat(self, user_id: str, thread_id: str) -> Optional[Dict[str, Any]]:
        user_chats = self.get_user_chats(user_id)
        return user_chats.get(thread_id)

    def create_or_update_research_session(
        self,
        user_id: str,
        thread_id: str,
        company_name: str,
        website_url: str,
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        user_chats = self.get_user_chats(user_id)
        now = datetime.utcnow().isoformat()
        
        if thread_id in user_chats:
            chat = user_chats[thread_id]
            chat["company_name"] = company_name
            chat["website_url"] = website_url
            chat["title"] = f"Research: {company_name}"
            chat["updated_at"] = now
            chat["research_data"] = research_data
        else:
            chat = {
                "thread_id": thread_id,
                "user_id": user_id,
                "company_name": company_name,
                "website_url": website_url,
                "title": f"Research: {company_name}",
                "created_at": now,
                "updated_at": now,
                "research_data": research_data,
                "messages": []
            }
            user_chats[thread_id] = chat

        # Add initial assistant report message if messages empty
        if not chat["messages"]:
            chat["messages"].append({
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "type": "research_report",
                "content": research_data.get("report", "Research process completed."),
                "timestamp": now,
                "metadata": {
                    "company_name": company_name,
                    "website_url": website_url
                }
            })

        self.save_to_disk()
        return chat

    def add_message(
        self,
        user_id: str,
        thread_id: str,
        role: str,
        content: str,
        msg_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        user_chats = self.get_user_chats(user_id)
        if thread_id not in user_chats:
            raise ValueError(f"Chat thread {thread_id} not found for user {user_id}")

        now = datetime.utcnow().isoformat()
        msg = {
            "id": str(uuid.uuid4()),
            "role": role,
            "type": msg_type,
            "content": content,
            "timestamp": now,
            "metadata": metadata or {}
        }
        user_chats[thread_id]["messages"].append(msg)
        user_chats[thread_id]["updated_at"] = now
        self.save_to_disk()
        return msg

    def delete_chat(self, user_id: str, thread_id: str) -> bool:
        user_chats = self.get_user_chats(user_id)
        if thread_id in user_chats:
            del user_chats[thread_id]
            self.save_to_disk()
            return True
        return False


chat_store = ChatStore()
