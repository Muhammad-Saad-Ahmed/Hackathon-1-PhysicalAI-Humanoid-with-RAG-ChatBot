from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum
import uuid


class SectionType(str, Enum):
    TEXT = "text"
    CODE = "code"
    DIAGRAM = "diagram"
    EXERCISE = "exercise"
    SUMMARY = "summary"


class SectionBase(BaseModel):
    chapter_id: str
    title: str
    content: str
    position: int
    section_type: SectionType


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    position: Optional[int] = None
    section_type: Optional[SectionType] = None


class Section(SectionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True