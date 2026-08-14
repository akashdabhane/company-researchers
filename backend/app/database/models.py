import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    thread_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, default="anonymous")
    company_name = Column(String, nullable=False)
    website_url = Column(String, nullable=True)
    research_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship to messages
    messages = relationship(
        "ChatMessageModel",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessageModel.timestamp"
    )

    def to_summary_dict(self):
        return {
            "thread_id": self.thread_id,
            "company_name": self.company_name,
            "website_url": self.website_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_detail_dict(self):
        return {
            "thread_id": self.thread_id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "website_url": self.website_url,
            "research_data": self.research_data or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "messages": [m.to_dict() for m in self.messages]
        }


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, index=True)
    thread_id = Column(String, ForeignKey("chat_sessions.thread_id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False, default="anonymous")
    role = Column(String, nullable=False)  # user, assistant, system
    type = Column(String, nullable=False, default="text")  # text, research_report
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship to session
    session = relationship("ChatSessionModel", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "role": self.role,
            "type": self.type,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
