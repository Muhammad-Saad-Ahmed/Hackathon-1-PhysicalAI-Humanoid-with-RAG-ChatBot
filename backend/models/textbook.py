from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import uuid


class TextbookStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class TextbookBase(BaseModel):
    title: str
    subject_area: str
    target_audience: str
    description: Optional[str] = None
    status: TextbookStatus = TextbookStatus.DRAFT
    generation_params: dict  # serialized generation parameters
    export_formats: List[str] = []


class TextbookCreate(TextbookBase):
    pass


class TextbookUpdate(BaseModel):
    title: Optional[str] = None
    subject_area: Optional[str] = None
    target_audience: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TextbookStatus] = None
    generation_params: Optional[dict] = None


class Textbook(TextbookBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True