from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..database.repositories import TextbookRepository, ChapterRepository, SectionRepository
from ..vector_store.embedding_service import EmbeddingService
from ..vector_store.qdrant_client import QdrantService
from ..models.textbook import TextbookStatus

# Constants for chunking
DEFAULT_CHUNK_SIZE = 500  # characters
DEFAULT_CHUNK_OVERLAP = 50 # characters

class ContentIndexingService:
    """
    Service for indexing textbook content into the vector store.
    """

    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def _chunk_text(self, text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
        """
        Splits a given text into smaller chunks with optional overlap.
        A simple character-based chunking strategy.

        Args:
            text: The input text to chunk.
            chunk_size: The maximum size of each chunk in characters.
            chunk_overlap: The number of characters to overlap between consecutive chunks.

        Returns:
            A list of text chunks.
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += (chunk_size - chunk_overlap)
            # Ensure we don't go past the end if the next start would be too far
            if start >= len(text) - chunk_overlap:
                break
        return chunks

    def index_textbook(self, textbook_id: str):
        """
        Indexes all content of a given textbook.

        Args:
            textbook_id: The ID of the textbook to index.
        """
        textbook = TextbookRepository.get(self.db, textbook_id)
        if not textbook or textbook.status != TextbookStatus.COMPLETED:
            raise ValueError("Textbook not found or not completed.")

        # First, clear any existing vectors for this textbook to avoid duplicates
        self.qdrant_service.delete_by_textbook_id(textbook_id)

        # Get all chapters and their sections
        chapters = ChapterRepository.get_by_textbook(self.db, textbook_id)
        
        all_chunks_to_store = []

        for chapter in chapters:
            sections = SectionRepository.get_by_chapter(self.db, chapter.id)
            for section in sections:
                base_content = f"Chapter: {chapter.title}\nSection: {section.title}\n\n"
                
                # Apply chunking to the section's content
                section_chunks = self._chunk_text(section.content)

                for i, chunk_text in enumerate(section_chunks):
                    # Prepend chapter and section titles to each chunk for context
                    full_chunk_text = base_content + chunk_text
                    
                    # Generate embedding
                    embedding = self.embedding_service.embed_text(full_chunk_text)

                    # Prepare the chunk for storage
                    chunk_data = {
                        "content_id": section.id, # Still link to the section ID
                        "content_type": "section_chunk", # Indicate it's a chunk of a section
                        "textbook_id": textbook_id,
                        "chapter_id": chapter.id,
                        "text": full_chunk_text,
                        "embedding": embedding,
                        "metadata": {
                            "title": section.title,
                            "chapter_title": chapter.title,
                            "chunk_index": i, # Keep track of chunk order
                        }
                    }
                    all_chunks_to_store.append(chunk_data)

        # Store all chunks in Qdrant in a single batch
        if all_chunks_to_store:
            self.qdrant_service.store_text_chunks(all_chunks_to_store)
