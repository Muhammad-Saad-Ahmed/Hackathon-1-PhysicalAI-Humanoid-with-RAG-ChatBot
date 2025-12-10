from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
import uuid
from ...models.textbook_generation import GenerateTextbookRequest # Import GenerateTextbookRequest

class GenerationParameterBase(BaseModel):
    name: str
    value: str
    textbook_id: Optional[str] = None


class GenerationParameterCreate(GenerationParameterBase):
    pass


class GenerationParameterUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    textbook_id: Optional[str] = None


class GenerationParameter(GenerationParameterBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- New models for Saved Generation Parameter Sets ---

class SavedGenerationParameterSetBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] # Stores the GenerateTextbookRequest.dict()


class SavedGenerationParameterSetCreate(SavedGenerationParameterSetBase):
    pass


class SavedGenerationParameterSetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class SavedGenerationParameterSet(SavedGenerationParameterSetBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True