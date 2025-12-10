import logging
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.chat_message import ChatQueryRequest, ChatQueryResponse, ChatMessageCreate
from ...models.chat_session import ChatSessionCreate
from ...database.repositories import ChatSessionRepository, ChatMessageRepository
from ...services.rag_service import RAGService
from ...services.llm_service import LLMService
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=ChatQueryResponse)
async def chat_query(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """Handle chat queries using RAG."""
    
    if not request.textbook_id:
        raise HTTPException(status_code=400, detail="textbook_id is required.")
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        logger.info(f"Received chat query for textbook {request.textbook_id}: '{request.query}'")
        rag_service = RAGService()
        llm_service = LLMService()

        # Handle chat session
        session_id = request.session_id
        if session_id:
            chat_session = ChatSessionRepository.get(db, session_id)
            if not chat_session:
                raise HTTPException(status_code=404, detail="Chat session not found.")
        else:
            chat_session_create = ChatSessionCreate(textbook_id=request.textbook_id)
            chat_session = ChatSessionRepository.create(db, chat_session_create)
            session_id = chat_session.id
        
        # Store user's message
        user_message_create = ChatMessageCreate(
            session_id=session_id,
            role="user",
            content=request.query,
            context_snippet=request.context_id
        )
        ChatMessageRepository.create(db, user_message_create)

        # RAG process
        search_results = rag_service.search(query=request.query, textbook_id=request.textbook_id)
        context = "\n---\n".join([result['text'] for result in search_results])
        if not context:
            context = "No relevant context found."

        response_text = await llm_service.generate_chat_response(query=request.query, context=context)
        
        sources = [{"content_id": r["content_id"], "title": r["metadata"].get("title"), "relevance_score": r["score"]} for r in search_results]

        # Store LLM's response
        assistant_message_create = ChatMessageCreate(
            session_id=session_id,
            role="assistant",
            content=response_text,
            context_snippet=context
        )
        ChatMessageRepository.create(db, assistant_message_create)
        
        logger.info(f"Successfully generated response for session {session_id}")
        return ChatQueryResponse(response=response_text, sources=sources, session_id=session_id)

    except Exception as e:
        logger.error(f"Error processing chat query for textbook {request.textbook_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing chat query: {str(e)}")


@router.post("/stream", response_class=StreamingResponse)
async def chat_query_stream(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """Handle chat queries using RAG with streaming responses."""

    if not request.textbook_id:
        raise HTTPException(status_code=400, detail="textbook_id is required.")
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    async def generate_response_stream():
        full_response_content = ""
        session_id = request.session_id
        try:
            logger.info(f"Streaming chat query for textbook {request.textbook_id}: '{request.query}'")
            rag_service = RAGService()
            llm_service = LLMService()

            if session_id:
                if not ChatSessionRepository.get(db, session_id):
                    raise HTTPException(status_code=404, detail="Chat session not found.")
            else:
                chat_session = ChatSessionRepository.create(db, ChatSessionCreate(textbook_id=request.textbook_id))
                session_id = chat_session.id
            
            ChatMessageRepository.create(db, ChatMessageCreate(session_id=session_id, role="user", content=request.query, context_snippet=request.context_id))

            search_results = rag_service.search(query=request.query, textbook_id=request.textbook_id)
            context = "\n---\n".join([r['text'] for r in search_results]) or "No relevant context found."

            initial_data = {
                "session_id": session_id,
                "sources": [{"content_id": r["content_id"], "title": r["metadata"].get("title"), "relevance_score": r["score"]} for r in search_results]
            }
            yield f"data: {json.dumps(initial_data)}\n\n"

            async for chunk in llm_service.generate_chat_response(query=request.query, context=context):
                full_response_content += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n"

            ChatMessageRepository.create(db, ChatMessageCreate(session_id=session_id, role="assistant", content=full_response_content, context_snippet=context))
            logger.info(f"Successfully streamed response for session {session_id}")

        except HTTPException as e:
            logger.error(f"HTTP exception in chat stream for textbook {request.textbook_id}: {e.detail}", exc_info=True)
            yield f"data: {json.dumps({'error': e.detail, 'status_code': e.status_code})}\n\n"
        except Exception as e:
            logger.error(f"Exception in chat stream for textbook {request.textbook_id}: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': f'Error processing chat query: {str(e)}', 'status_code': 500})}\n\n"
        finally:
            db.close()

    return StreamingResponse(generate_response_stream(), media_type="text/event-stream")


@router.get("/sessions")
def get_chat_sessions(db: Session = Depends(get_db)):
    """Get chat sessions."""
    logger.warning("Attempted to access non-implemented /sessions endpoint.")
    raise HTTPException(status_code=501, detail="Not implemented yet")