from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...models.index import IndexRequest
from ...services.content_indexing import ContentIndexingService
from ...api.dependencies import get_api_key # Import the new dependency


router = APIRouter()


@router.post("/", dependencies=[Depends(get_api_key)]) # Add dependency here
async def trigger_indexing(
    request: IndexRequest,
    db: Session = Depends(get_db)
):
    """Trigger textbook content indexing for RAG."""
    try:
        indexing_service = ContentIndexingService(db)
        indexing_service.index_textbook(request.textbook_id)
        return {"message": f"Indexing for textbook_id {request.textbook_id} triggered successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering indexing: {str(e)}")