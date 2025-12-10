from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime


class StylePreferences(BaseModel):
    include_exercises: bool = True
    include_summaries: bool = True
    include_diagrams: bool = True


class FormatPreferences(BaseModel):
    font_size: str = "medium"  # small, medium, large
    layout: str = "standard"  # standard, compact, spacious


class GenerateTextbookRequest(BaseModel):
    subject_area: str
    target_audience: str
    chapter_topics: List[str]
    style_preferences: Optional[StylePreferences] = None
    format_preferences: Optional[FormatPreferences] = None


class GenerateTextbookResponse(BaseModel):
    textbook_id: str
    status: str  # success, queued, error
    estimated_completion: Optional[int] = None  # seconds


class TextbookGenerationStatus(BaseModel):
    textbook_id: str
    status: str  # draft, generating, completed, failed
    progress: float  # 0.0 to 1.0
    message: str