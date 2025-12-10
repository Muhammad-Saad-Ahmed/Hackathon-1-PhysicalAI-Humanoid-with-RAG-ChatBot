from pydantic import BaseModel

class IndexRequest(BaseModel):
    textbook_id: str
