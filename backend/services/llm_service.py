from typing import Dict, Any, List, Optional, AsyncGenerator
from groq import Groq
from ..config.settings import settings
import json


class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL

    async def generate_chapter_content(
        self,
        topic: str,
        subject_area: str,
        target_audience: str,
        include_exercises: bool = True,
        include_summaries: bool = True,
        include_diagrams: bool = True,
        format_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate chapter content using LLM.

        Args:
            topic: The topic for the chapter
            subject_area: The subject area of the textbook
            target_audience: The target audience level
            include_exercises: Whether to include exercises
            include_summaries: Whether to include summaries
            include_diagrams: Whether to include diagrams

        Returns:
            Dictionary containing the generated content and structure
        """
        # Create a prompt for the LLM
        prompt = self._create_chapter_prompt(
            topic=topic,
            subject_area=subject_area,
            target_audience=target_audience,
            include_exercises=include_exercises,
            include_summaries=include_summaries,
            include_diagrams=include_diagrams,
            format_preferences=format_preferences
        )

        try:
            # Call the LLM to generate content
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )

            content = chat_completion.choices[0].message.content

            # Parse the content to extract sections if needed
            return {
                "content": content,
                "sections": []  # For now, return empty sections; in a full implementation, we'd parse the content
            }
        except Exception as e:
            raise Exception(f"Error generating chapter content: {str(e)}")

    async def generate_textbook_overview(
        self,
        subject_area: str,
        target_audience: str,
        chapter_topics: List[str]
    ) -> str:
        """
        Generate an overview for the entire textbook.

        Args:
            subject_area: The subject area of the textbook
            target_audience: The target audience level
            chapter_topics: List of chapter topics

        Returns:
            Overview text for the textbook
        """
        prompt = f"""
        Create a brief overview for a textbook on {subject_area} for {target_audience} students.
        The textbook will cover the following topics: {', '.join(chapter_topics)}.
        The overview should be engaging and provide context for why these topics are important.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating textbook overview: {str(e)}")

    def _create_chapter_prompt(
        self,
        topic: str,
        subject_area: str,
        target_audience: str,
        include_exercises: bool,
        include_summaries: bool,
        include_diagrams: bool,
        format_preferences: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a prompt for generating chapter content.

        Args:
            topic: The topic for the chapter
            subject_area: The subject area of the textbook
            target_audience: The target audience level
            include_exercises: Whether to include exercises
            include_summaries: Whether to include summaries
            include_diagrams: Whether to include diagrams
            format_preferences: Optional dictionary of format preferences (e.g., font_size, layout)

        Returns:
            Formatted prompt string
        """
        prompt = f"""
        Write a comprehensive chapter on "{topic}" for a textbook on {subject_area}
        aimed at {target_audience} students. The chapter should include:

        1. An engaging introduction that connects to previous knowledge
        2. Main content with clear explanations and examples
        3. A summary of key points"""

        if include_exercises:
            prompt += """
        4. Practice exercises with solutions"""

        if include_summaries:
            prompt += """
        5. Key terms and definitions"""

        if include_diagrams:
            prompt += """
        6. Suggestions for diagrams or visual aids that would help explain concepts"""

        if format_preferences:
            if format_preferences.get("font_size"):
                prompt += f"""

        The content should be structured to be compatible with a {format_preferences['font_size']} font size."""
            if format_preferences.get("layout"):
                prompt += f"""
        Consider a {format_preferences['layout']} layout when structuring the content, ensuring readability and flow."""

        prompt += f"""

        Ensure the content is appropriate for {target_audience} students, with
        explanations that match their comprehension level. Use clear, engaging
        language and include real-world applications where relevant.
        """

        return prompt

    async def break_down_topic(self, topic: str, subject_area: str, target_audience: str) -> List[str]:
        """
        Break down a complex topic into a list of subtopics.
        Args:
            topic: The complex topic to break down.
            subject_area: The subject area for context.
            target_audience: The target audience level.
        Returns:
            A list of subtopics.
        """
        prompt = f"""
        Break down the following complex topic into a list of smaller, more manageable subtopics for a textbook chapter.
        The textbook is on "{subject_area}" for a "{target_audience}" audience.
        The main topic is: "{topic}"

        Return a JSON array of strings, where each string is a subtopic.
        For example:
        ["Subtopic 1", "Subtopic 2", "Subtopic 3"]
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )

            response_content = chat_completion.choices[0].message.content
            # The response is a JSON string, so we need to parse it.
            # The prompt asks for a list of strings, but the model might return a dictionary with a key.
            # Let's assume it returns a JSON object with a "subtopics" key.
            subtopics = json.loads(response_content).get("subtopics", [])
            if not subtopics:
                # If the model returns a flat list
                subtopics = json.loads(response_content)

            if isinstance(subtopics, list):
                return subtopics
            else:
                return [topic] # Fallback to the original topic

        except Exception as e:
            # If the LLM fails or returns a malformed response, fallback to the original topic.
            return [topic]

    async def validate_content_accuracy(self, content: str, subject_area: str) -> List[str]:
        """
        Validate the factual accuracy of generated content.

        Args:
            content: The content to validate
            subject_area: The subject area for context

        Returns:
            List of potential accuracy issues found
        """
        prompt = f"""
        Review the following content from a {subject_area} textbook for factual accuracy.
        Identify any potential inaccuracies, outdated information, or misleading statements:

        {content}

        Return a list of potential issues, or an empty list if no issues are found.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )

            # Parse the response to extract issues
            response = chat_completion.choices[0].message.content
            # In a real implementation, we'd parse this more carefully
            return [response] if response.strip() else []
        except Exception as e:
            raise Exception(f"Error validating content accuracy: {str(e)}")

        async def validate_content_coherence(self, content: str, target_audience: str) -> List[str]:

            """

            Validate the coherence and pedagogical appropriateness of generated content.

    

            Args:

                content: The content to validate

                target_audience: The target audience level

    

            Returns:

                List of potential coherence/appropriateness issues found

            """

            prompt = f"""

            Review the following content from a {target_audience} level textbook for:

            1. Coherence and logical flow

            2. Pedagogical appropriateness for {target_audience} students

            3. Clarity and readability

            4. Appropriate complexity level

    

            Content to review:

            {content}

    

            Return a list of potential issues related to coherence or pedagogical appropriateness,

            or an empty list if no issues are found.

            """

    

            try:

                chat_completion = self.client.chat.completions.create(

                    messages=[

                        {

                            "role": "user",

                            "content": prompt,

                        }

                    ],

                    model=self.model,

                )

    

                # Parse the response to extract issues

                response = chat_completion.choices[0].message.content

                # In a real implementation, we'd parse this more carefully

                return [response] if response.strip() else []

            except Exception as e:

                raise Exception(f"Error validating content coherence: {str(e)}")

    

    async def generate_chat_response(self, query: str, context: str) -> AsyncGenerator[str, None]:
        """
        Generate a chat response based on a query and retrieved context, streaming the response.

        Args:
            query: The user's query.
            context: The retrieved content from the vector store.

        Returns:
            An async generator that yields chunks of the generated chat response.
        """
        prompt = f"""
        You are a helpful assistant for a textbook.
        A user has asked the following question: "{query}"

        Here is some relevant context from the textbook:
        ---
        {context}
        ---

        Based on this context, please provide a concise and helpful answer to the user's question.
        If the context does not contain the answer, say that you don't have enough information to answer.
        """

        try:
            stream = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                stream=True, # Enable streaming
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(f"Error generating streaming chat response: {str(e)}")