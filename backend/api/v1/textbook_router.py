import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Union, Optional
from ...database.database import get_db
from ...models.textbook import TextbookCreate, Textbook, TextbookUpdate
from ...models.textbook_generation import GenerateTextbookRequest, GenerateTextbookResponse, TextbookGenerationStatus
from ...database.repositories import TextbookRepository, ChapterRepository
from ...services.textbook_generation import TextbookGenerationService
from ...services.export_service import ExportService
from ...main import limiter
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=Textbook)
@limiter.limit("10/minute")
def create_textbook(
    request: Request,
    textbook: TextbookCreate,
    db: Session = Depends(get_db)
):
    """Create a new textbook."""
    logger.info(f"Creating new textbook with title: {textbook.title}")
    return TextbookRepository.create(db, textbook)


@router.post("/generate", response_model=GenerateTextbookResponse)
@limiter.limit("5/minute")
async def generate_textbook(
    request: Request,
    gen_request: GenerateTextbookRequest,
    db: Session = Depends(get_db)
):
    """Generate a new textbook based on the provided parameters."""
    # Sanitize and validate inputs
    gen_request.subject_area = gen_request.subject_area.strip()
    gen_request.target_audience = gen_request.target_audience.strip()
    gen_request.chapter_topics = [topic.strip() for topic in gen_request.chapter_topics if topic.strip()]

    if not gen_request.subject_area:
        raise HTTPException(status_code=400, detail="Subject area cannot be empty.")
    if not gen_request.target_audience:
        raise HTTPException(status_code=400, detail="Target audience cannot be empty.")
    if not gen_request.chapter_topics:
        raise HTTPException(status_code=400, detail="Chapter topics cannot be empty.")
        
    try:
        logger.info(f"Starting textbook generation for subject: {gen_request.subject_area}")
        service = TextbookGenerationService(db)
        result = await service.generate_textbook(gen_request)
        logger.info(f"Successfully initiated textbook generation with ID: {result['textbook_id']}")
        return GenerateTextbookResponse(
            textbook_id=result["textbook_id"],
            status=result["status"]
        )
    except Exception as e:
        logger.error(f"Error generating textbook for subject '{gen_request.subject_area}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating textbook: {str(e)}")


@router.get("/generation-status/{textbook_id}", response_model=TextbookGenerationStatus)
@limiter.limit("60/minute")
def get_generation_status(
    request: Request,
    textbook_id: str,
    db: Session = Depends(get_db)
):
    """Get the status of textbook generation."""
    service = TextbookGenerationService(db)
    status = service.get_generation_status(textbook_id)
    return TextbookGenerationStatus(
        textbook_id=status["textbook_id"],
        status=status["status"],
        progress=status["progress"],
        message=status["message"]
    )


@router.get("/{textbook_id}", response_model=Textbook)
@limiter.limit("60/minute")
def get_textbook(
    request: Request,
    textbook_id: str,
    db: Session = Depends(get_db)
):
    """Get a textbook by ID."""
    db_textbook = TextbookRepository.get(db, textbook_id)
    if not db_textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    return db_textbook


@router.get("/", response_model=List[Textbook])
@limiter.limit("60/minute")
def get_textbooks(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get a list of textbooks."""
    return TextbookRepository.get_all(db, skip=skip, limit=limit)


@router.put("/{textbook_id}", response_model=Textbook)
@limiter.limit("10/minute")
def update_textbook(
    request: Request,
    textbook_id: str,
    textbook_update: TextbookUpdate,
    db: Session = Depends(get_db)
):
    """Update a textbook."""
    db_textbook = TextbookRepository.update(db, textbook_id, textbook_update)
    if not db_textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    return db_textbook


@router.delete("/{textbook_id}")
@limiter.limit("10/minute")
def delete_textbook(
    request: Request,
    textbook_id: str,
    db: Session = Depends(get_db)
):
    """Delete a textbook."""
    logger.info(f"Attempting to delete textbook with ID: {textbook_id}")
    success = TextbookRepository.delete(db, textbook_id)
    if not success:
        logger.warning(f"Failed to delete textbook with ID: {textbook_id} - not found.")
        raise HTTPException(status_code=404, detail="Textbook not found")
    logger.info(f"Successfully deleted textbook with ID: {textbook_id}")
    return {"message": "Textbook deleted successfully"}


@router.post("/{textbook_id}/export")
@limiter.limit("5/minute")
async def export_textbook(
    request: Request,
    textbook_id: str,
    format: str = Query(..., regex="^(pdf|epub)$"),
    db: Session = Depends(get_db)
):
    """
    Export a textbook in a specific format (PDF or ePub).
    """
    logger.info(f"Export requested for textbook {textbook_id} in format {format}")
    textbook = TextbookRepository.get(db, textbook_id)
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    
    if textbook.status != "completed":
        raise HTTPException(status_code=400, detail="Textbook generation is not yet completed.")

    chapters = ChapterRepository.get_by_textbook_id(db, textbook_id)
    if not chapters:
        raise HTTPException(status_code=404, detail="No chapters found for this textbook.")

    format_preferences = textbook.generation_params.get("format_preferences") if textbook.generation_params else {}

    export_service = ExportService()
    try:
        if format == "pdf":
            full_markdown_content = "\n\n".join([chapter.content for chapter in chapters])
            pdf_bytes = export_service.export_to_pdf(full_markdown_content, format_preferences=format_preferences)
            return StreamingResponse(
                content=iter([pdf_bytes]),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=\"{textbook.title.replace(' ', '_')}.pdf\""}
            )
        elif format == "epub":
            chapter_data = [(chapter.title, chapter.content) for chapter in chapters]
            epub_bytes = export_service.export_to_epub(textbook.title, textbook.subject_area, chapter_data, format_preferences=format_preferences)
            return StreamingResponse(
                content=iter([epub_bytes]),
                media_type="application/epub+zip",
                headers={"Content-Disposition": f"attachment; filename=\"{textbook.title.replace(' ', '_')}.epub\""}
            )
    except Exception as e:
        logger.error(f"Failed to export textbook {textbook_id} to {format}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to export textbook.")

    raise HTTPException(status_code=400, detail="Invalid export format specified.")