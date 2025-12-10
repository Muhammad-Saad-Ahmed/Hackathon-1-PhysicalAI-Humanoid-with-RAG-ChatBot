from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid


class ChapterBase(BaseModel):
    textbook_id: str
    title: str
    slug: str
    content: str
    position: int
    word_count: Optional[int] = None
    reading_time: Optional[int] = None  # estimated in minutes


class ChapterCreate(ChapterBase):
    pass


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    position: Optional[int] = None
    word_count: Optional[int] = None
    reading_time: Optional[int] = None


class Chapter(ChapterBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True