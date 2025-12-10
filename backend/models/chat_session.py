from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid


class ChatSessionBase(BaseModel):
    textbook_id: Optional[str] = None
    chapter_id: Optional[str] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    textbook_id: Optional[str] = None
    chapter_id: Optional[str] = None


class ChatSession(ChatSessionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True