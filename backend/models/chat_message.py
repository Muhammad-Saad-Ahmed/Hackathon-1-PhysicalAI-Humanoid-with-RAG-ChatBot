from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum
import uuid


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessageBase(BaseModel):
    session_id: str
    role: MessageRole
    content: str
    context_snippet: Optional[str] = None  # the selected text that triggered the question


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageUpdate(BaseModel):
    role: Optional[MessageRole] = None
    content: Optional[str] = None
    context_snippet: Optional[str] = None


class ChatMessage(ChatMessageBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True