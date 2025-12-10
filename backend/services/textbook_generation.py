from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from ..models.textbook import TextbookCreate, TextbookUpdate, TextbookStatus
from ..models.chapter import ChapterCreate
from ..models.section import SectionCreate, SectionType
from ..database.repositories import TextbookRepository, ChapterRepository, SectionRepository
from ..models.textbook_generation import GenerateTextbookRequest
from .llm_service import LLMService
from ..config.settings import settings


class TextbookGenerationService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        # Track progress for each textbook
        self.progress_tracking = {}

    async def generate_textbook(self, request: GenerateTextbookRequest) -> Dict[str, Any]:
        """
        Generate a textbook based on the provided parameters.

        Args:
            request: GenerateTextbookRequest containing subject area, target audience, and chapter topics

        Returns:
            Dictionary with textbook_id and status
        """
        try:
            # Create a new textbook record
            textbook_data = {
                "title": f"{request.subject_area} - {request.target_audience}",
                "subject_area": request.subject_area,
                "target_audience": request.target_audience,
                "status": TextbookStatus.GENERATING,
                "generation_params": request.dict()
            }

            textbook_create = TextbookCreate(**textbook_data)
            textbook = TextbookRepository.create(self.db, textbook_create)

            # Initialize progress tracking for this textbook
            total_chapters = len(request.chapter_topics)
            self.progress_tracking[textbook.id] = {
                "current": 0,
                "total": total_chapters,
                "message": "Starting textbook generation"
            }

            # Update status to generating
            TextbookRepository.update(self.db, textbook.id,
                                    TextbookUpdate(status=TextbookStatus.GENERATING))

            # Generate chapters based on the requested topics
            for idx, topic in enumerate(request.chapter_topics):
                self.progress_tracking[textbook.id]["message"] = f"Generating chapter {idx + 1} of {total_chapters}: {topic}"
                await self._generate_chapter(textbook.id, topic, idx + 1, request)
                self.progress_tracking[textbook.id]["current"] = idx + 1

            # Update status to completed
            TextbookRepository.update(self.db, textbook.id,
                                    TextbookUpdate(status=TextbookStatus.COMPLETED, export_formats=["pdf", "epub"]))

            # Clear progress tracking
            if textbook.id in self.progress_tracking:
                del self.progress_tracking[textbook.id]

            return {
                "textbook_id": textbook.id,
                "status": "success"
            }

        except Exception as e:
            # Update status to failed
            TextbookRepository.update(self.db, textbook.id,
                                    TextbookUpdate(status=TextbookStatus.FAILED))
            # Clear progress tracking on failure
            if textbook.id in self.progress_tracking:
                del self.progress_tracking[textbook.id]
            raise e

    async def _generate_chapter(self, textbook_id: str, topic: str, position: int, request: GenerateTextbookRequest):
        """
        Generate a single chapter for the textbook.

        Args:
            textbook_id: ID of the textbook to add the chapter to
            topic: Topic for the chapter
            position: Position of the chapter in the textbook
            request: Original generation request
        """
        # For large requests, we may need to chunk the generation process
        # In this implementation, we'll check if the topic is complex and might require chunking
        # For now, we'll just call the LLM service directly, but in a full implementation
        # we would chunk complex topics into subtopics if needed
        chapter_content = await self._generate_chapter_content_with_chunking(
            topic=topic,
            subject_area=request.subject_area,
            target_audience=request.target_audience,
            include_exercises=request.style_preferences.include_exercises if request.style_preferences else True,
            include_summaries=request.style_preferences.include_summaries if request.style_preferences else True,
            include_diagrams=request.style_preferences.include_diagrams if request.style_preferences else True,
            format_preferences=request.format_preferences.dict() if request.format_preferences else None
        )

        # Structure the content with proper headings and sections
        structured_content = self._structure_chapter_content(
            topic=topic,
            raw_content=chapter_content["content"],
            include_exercises=request.style_preferences.include_exercises if request.style_preferences else True,
            include_summaries=request.style_preferences.include_summaries if request.style_preferences else True
        )

        # Validate content for coherence and pedagogical appropriateness
        coherence_issues = await self.llm_service.validate_content_coherence(
            content=structured_content,
            target_audience=request.target_audience
        )

        # Validate content for factual accuracy
        accuracy_issues = await self.llm_service.validate_content_accuracy(
            content=structured_content,
            subject_area=request.subject_area
        )

        # Log any issues found (in a real implementation, we might want to handle these differently)
        all_issues = coherence_issues + accuracy_issues
        if all_issues:
            print(f"Issues found in chapter '{topic}': {all_issues}")

        # Create chapter
        chapter_data = {
            "textbook_id": textbook_id,
            "title": topic,
            "slug": topic.lower().replace(" ", "-").replace("_", "-"),
            "content": structured_content,
            "position": position,
            "word_count": len(structured_content.split()),
            "reading_time": len(structured_content.split()) // 200  # approx 200 words per minute
        }

        chapter_create = ChapterCreate(**chapter_data)
        chapter = ChapterRepository.create(self.db, chapter_create)

        # Create sections within the chapter based on the structured content
        sections = self._extract_sections_from_content(structured_content)
        for section_idx, section_data in enumerate(sections):
            section_create = SectionCreate(
                chapter_id=chapter.id,
                title=section_data["title"],
                content=section_data["content"],
                position=section_idx + 1,
                section_type=section_data["type"]
            )
            SectionRepository.create(self.db, section_create)

    def _structure_chapter_content(self, topic: str, raw_content: str, include_exercises: bool, include_summaries: bool) -> str:
        """
        Structure the raw content with proper headings, sections, and pedagogical elements.

        Args:
            topic: The topic of the chapter
            raw_content: Raw content from the LLM
            include_exercises: Whether to include exercises
            include_summaries: Whether to include summaries

        Returns:
            Structured content with proper formatting
        """
        # Add proper chapter heading
        structured = f"# {topic}\n\n"

        # Add introduction
        structured += "## Introduction\n"
        structured += self._extract_introduction(raw_content) + "\n\n"

        # Add main content sections
        main_content = self._extract_main_content(raw_content)
        structured += "## Main Content\n"
        structured += main_content + "\n\n"

        # Add summary if requested
        if include_summaries:
            structured += "## Summary\n"
            structured += self._extract_summary(raw_content) + "\n\n"

        # Add exercises if requested
        if include_exercises:
            structured += "## Exercises\n"
            structured += self._generate_exercises(topic) + "\n\n"

        return structured

    def _extract_introduction(self, content: str) -> str:
        """
        Extract or generate an introduction from the content.
        """
        # In a real implementation, this would use NLP to extract the introduction
        # For now, we'll return the first few sentences
        sentences = content.split('. ')
        intro = '. '.join(sentences[:3]) + '.'
        return intro

    def _extract_main_content(self, content: str) -> str:
        """
        Extract the main content, organizing it into subsections.
        """
        # In a real implementation, this would use NLP to identify sections
        # For now, we'll return the content as is
        return content

    def _extract_summary(self, content: str) -> str:
        """
        Extract or generate a summary from the content.
        """
        # In a real implementation, this would summarize the content
        # For now, we'll return the last few sentences
        sentences = content.split('. ')
        summary = '. '.join(sentences[-3:]) + '.'
        return summary

    def _generate_exercises(self, topic: str) -> str:
        """
        Generate exercises based on the topic.
        """
        # In a real implementation, this would generate exercises using the LLM
        # For now, we'll return placeholder exercises
        return f"1. Define the key concepts in {topic}.\n2. Explain the main principles of {topic}.\n3. Provide an example of how {topic} is applied in practice."

    def _extract_sections_from_content(self, content: str) -> List[Dict[str, str]]:
        """
        Extract sections from the structured content.

        Args:
            content: The structured chapter content

        Returns:
            List of sections with title, content, and type
        """
        sections = []

        # Split content by markdown headers
        lines = content.split('\n')
        current_section = {"title": "Introduction", "content": "", "type": SectionType.TEXT}

        for line in lines:
            if line.startswith('# '):  # Main title
                continue
            elif line.startswith('## '):  # Section header
                # Save the previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section)

                # Start a new section
                current_section = {
                    "title": line[3:].strip(),  # Remove '## ' prefix
                    "content": "",
                    "type": self._determine_section_type(line[3:].strip())
                }
            else:
                # Add content to the current section
                current_section["content"] += line + "\n"

        # Add the last section if it has content
        if current_section["content"].strip():
            sections.append(current_section)

        return sections

    def _determine_section_type(self, section_title: str) -> SectionType:
        """
        Determine the type of section based on its title.

        Args:
            section_title: The title of the section

        Returns:
            The appropriate SectionType
        """
        title_lower = section_title.lower()

        if "exercise" in title_lower or "problem" in title_lower or "question" in title_lower:
            return SectionType.EXERCISE
        elif "summary" in title_lower or "review" in title_lower:
            return SectionType.SUMMARY
        elif "code" in title_lower or "program" in title_lower:
            return SectionType.CODE
        elif "diagram" in title_lower or "figure" in title_lower or "image" in title_lower:
            return SectionType.DIAGRAM
        else:
            return SectionType.TEXT

    async def _generate_chapter_content_with_chunking(self, topic: str, subject_area: str, target_audience: str,
                                                      include_exercises: bool, include_summaries: bool, include_diagrams: bool,
                                                      format_preferences: Optional[Dict[str, Any]] = None):
        """
        Generate chapter content, with chunking for large/complex topics.

        Args:
            topic: The topic for the chapter
            subject_area: The subject area of the textbook
            target_audience: The target audience level
            include_exercises: Whether to include exercises
            include_summaries: Whether to include summaries
            include_diagrams: Whether to include diagrams
            format_preferences: Optional dictionary of format preferences (e.g., font_size, layout)

        Returns:
            Dictionary containing the generated content
        """
        # Determine if the topic is complex enough to require chunking
        # For simplicity, we'll use word count as a proxy for complexity
        topic_complexity_threshold = 5  # words
        topic_word_count = len(topic.split())

        if topic_word_count > topic_complexity_threshold:
            # For complex topics, break them down into subtopics
            subtopics = await self._break_down_complex_topic(topic, subject_area, target_audience)
            chapter_parts = []

            for subtopic in subtopics:
                part_content = await self.llm_service.generate_chapter_content(
                    topic=subtopic,
                    subject_area=subject_area,
                    target_audience=target_audience,
                    include_exercises=include_exercises,
                    include_summaries=include_summaries,
                    include_diagrams=include_diagrams,
                    format_preferences=format_preferences
                )
                chapter_parts.append(part_content)

            # Combine the parts into a single chapter
            combined_content = self._combine_chapter_parts(chapter_parts)
            return combined_content
        else:
            # For simple topics, generate content directly
            return await self.llm_service.generate_chapter_content(
                topic=topic,
                subject_area=subject_area,
                target_audience=target_audience,
                include_exercises=include_exercises,
                include_summaries=include_summaries,
                include_diagrams=include_diagrams,
                format_preferences=format_preferences
            )

    async def _break_down_complex_topic(self, topic: str, subject_area: str, target_audience: str) -> List[str]:
        """
        Break down a complex topic into subtopics.

        Args:
            topic: The complex topic to break down
            subject_area: The subject area
            target_audience: The target audience level

        Returns:
            List of subtopics
        """
        return await self.llm_service.break_down_topic(topic, subject_area, target_audience)

    def _combine_chapter_parts(self, parts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine multiple chapter parts into a single chapter.

        Args:
            parts: List of chapter parts

        Returns:
            Combined chapter content
        """
        # Combine all the content parts into a single chapter
        combined_content = ""
        all_sections = []

        for part in parts:
            combined_content += part.get("content", "") + "\n\n"
            all_sections.extend(part.get("sections", []))

        return {
            "content": combined_content.strip(),
            "sections": all_sections
        }

    def get_generation_status(self, textbook_id: str) -> Dict[str, Any]:
        """
        Get the status of textbook generation.

        Args:
            textbook_id: ID of the textbook to check

        Returns:
            Dictionary with status information
        """
        textbook = TextbookRepository.get(self.db, textbook_id)
        if not textbook:
            return {
                "textbook_id": textbook_id,
                "status": "not_found",
                "progress": 0.0,
                "message": "Textbook not found"
            }

        # Check if we have active progress tracking for this textbook
        if textbook_id in self.progress_tracking:
            tracking = self.progress_tracking[textbook_id]
            current = tracking["current"]
            total = tracking["total"]
            message = tracking["message"]

            if total > 0:
                progress = current / total
            else:
                progress = 0.0

            return {
                "textbook_id": textbook_id,
                "status": textbook.status.value,
                "progress": progress,
                "message": message
            }
        else:
            # Calculate progress based on status if no active tracking
            progress = 0.0
            message = f"Textbook is {textbook.status.value}"

            if textbook.status == TextbookStatus.COMPLETED:
                progress = 1.0
                message = "Textbook generation completed"
            elif textbook.status == TextbookStatus.GENERATING:
                progress = 0.5  # Default if we don't have specific progress
                message = "Textbook generation in progress"
            elif textbook.status == TextbookStatus.FAILED:
                progress = 0.0
                message = "Textbook generation failed"

            return {
                "textbook_id": textbook_id,
                "status": textbook.status.value,
                "progress": progress,
                "message": message
            }