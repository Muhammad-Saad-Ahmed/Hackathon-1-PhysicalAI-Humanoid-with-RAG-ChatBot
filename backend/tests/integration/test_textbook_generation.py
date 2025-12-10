import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.services.textbook_generation import TextbookGenerationService
from backend.models.textbook_generation import GenerateTextbookRequest, StylePreferences, FormatPreferences
from backend.models.textbook import TextbookStatus
from backend.models.chapter import ChapterCreate
import uuid

@pytest.mark.asyncio
async def test_generate_textbook_acceptance_scenario_1(mocker):
    """
    Given a user specifies "Physics" as subject and "High School" as target audience,
    When they request textbook generation,
    Then the system produces a structured textbook with appropriate physics content for high school students.
    """
    # Mock LLMService methods
    mock_llm_service = MagicMock()
    mock_llm_service.generate_chapter_content = AsyncMock(return_value={
        "content": "This is a chapter about a physics topic.",
        "sections": [{"title": "Section 1", "content": "Content of section 1"}]
    })
    mock_llm_service.validate_content_coherence = AsyncMock(return_value=[])
    mock_llm_service.validate_content_accuracy = AsyncMock(return_value=[])

    mocker.patch('backend.services.textbook_generation.LLMService', return_value=mock_llm_service)

    # Mock database session and repositories
    mock_db = MagicMock()
    mock_textbook_repo = MagicMock()
    mock_chapter_repo = MagicMock()
    mock_section_repo = MagicMock()

    # Mock repository create methods to return a mock object with an id
    mock_textbook_repo.create.return_value = MagicMock(id="test_textbook_id")
    mock_chapter_repo.create.return_value = MagicMock(id="test_chapter_id")
    mock_section_repo.create.return_value = MagicMock(id="test_section_id")

    # Mock the get method of textbook_repo to return the created textbook when update is called
    mock_textbook_repo.get.side_effect = [
        MagicMock(id="test_textbook_id", status=TextbookStatus.GENERATING),
        MagicMock(id="test_textbook_id", status=TextbookStatus.COMPLETED)
    ]
    # For chapter creation, simulate a created chapter with a content property
    def mock_chapter_create(db, chapter_create_data):
        mock_chapter = MagicMock(spec=ChapterCreate)
        mock_chapter.id = "test_chapter_id"
        mock_chapter.content = chapter_create_data.content
        return mock_chapter

    mock_chapter_repo.create.side_effect = mock_chapter_create


    mocker.patch('backend.services.textbook_generation.TextbookRepository', mock_textbook_repo)
    mocker.patch('backend.services.textbook_generation.ChapterRepository', mock_chapter_repo)
    mocker.patch('backend.services.textbook_generation.SectionRepository', mock_section_repo)

    # Instantiate the service
    service = TextbookGenerationService(db=mock_db)

    # Create a request
    request = GenerateTextbookRequest(
        subject_area="Physics",
        target_audience="High School",
        chapter_topics=["Introduction to Mechanics", "Thermodynamics"]
    )

    # Call the service
    result = await service.generate_textbook(request)

    # Assertions
    assert result["textbook_id"] == "test_textbook_id"
    assert result["status"] == "success"

    # Verify that the textbook was created with the correct status
    mock_textbook_repo.create.assert_called_once()
    # Check that the status was updated to GENERATING and then to COMPLETED
    assert mock_textbook_repo.update.call_count == 2
    
    # Verify chapter and section creation
    assert mock_chapter_repo.create.call_count == len(request.chapter_topics)
    assert mock_section_repo.create.call_count > 0

    # Verify LLM service calls
    assert mock_llm_service.generate_chapter_content.call_count == len(request.chapter_topics)
    assert mock_llm_service.validate_content_coherence.call_count == len(request.chapter_topics)
    assert mock_llm_service.validate_content_accuracy.call_count == len(request.chapter_topics)


@pytest.mark.asyncio
async def test_generate_textbook_acceptance_scenario_2(mocker):
    """
    Given a user specifies detailed chapter topics and learning objectives,
    When they request textbook generation,
    Then the system generates content that aligns with these specifications.
    """
    # Mock LLMService methods
    mock_llm_service = MagicMock()
    # Mock generate_chapter_content to return content that includes the topic
    mock_llm_service.generate_chapter_content.side_effect = lambda topic, **kwargs: {
        "content": f"Content for {topic}. This section explains {topic} in detail.",
        "sections": [{"title": f"Intro to {topic}", "content": f"Introduction to {topic}"}]
    }
    mock_llm_service.validate_content_coherence = AsyncMock(return_value=[])
    mock_llm_service.validate_content_accuracy = AsyncMock(return_value=[])

    mocker.patch('backend.services.textbook_generation.LLMService', return_value=mock_llm_service)

    # Mock database session and repositories
    mock_db = MagicMock()
    mock_textbook_repo = MagicMock()
    mock_chapter_repo = MagicMock()
    mock_section_repo = MagicMock()

    # Mock repository create methods to return a mock object with an id
    mock_textbook_repo.create.return_value = MagicMock(id="test_textbook_id_2")
    mock_chapter_repo.create.return_value = MagicMock(id="test_chapter_id_2")
    mock_section_repo.create.return_value = MagicMock(id="test_section_id_2")

    # Mock the get method of textbook_repo to return the created textbook when update is called
    mock_textbook_repo.get.side_effect = [
        MagicMock(id="test_textbook_id_2", status=TextbookStatus.GENERATING),
        MagicMock(id="test_textbook_id_2", status=TextbookStatus.COMPLETED)
    ]

    # For chapter creation, simulate a created chapter with a content property
    def mock_chapter_create_with_content(db, chapter_create_data):
        mock_chapter = MagicMock(spec=ChapterCreate)
        mock_chapter.id = str(uuid.uuid4()) # Use unique IDs for each chapter
        mock_chapter.content = chapter_create_data.content
        return mock_chapter

    mock_chapter_repo.create.side_effect = mock_chapter_create_with_content

    mocker.patch('backend.services.textbook_generation.TextbookRepository', mock_textbook_repo)
    mocker.patch('backend.services.textbook_generation.ChapterRepository', mock_chapter_repo)
    mocker.patch('backend.services.textbook_generation.SectionRepository', mock_section_repo)

    # Instantiate the service
    service = TextbookGenerationService(db=mock_db)

    # Create a request with detailed chapter topics
    detailed_topics = [
        "Quantum Physics: Wave-Particle Duality and Uncertainty Principle",
        "Classical Mechanics: Newton's Laws and Conservation of Energy"
    ]
    request = GenerateTextbookRequest(
        subject_area="Advanced Physics",
        target_audience="University Students",
        chapter_topics=detailed_topics
    )

    # Call the service
    result = await service.generate_textbook(request)

    # Assertions
    assert result["textbook_id"] == "test_textbook_id_2"
    assert result["status"] == "success"

    # Verify LLM service calls and content alignment
    assert mock_llm_service.generate_chapter_content.call_count == len(detailed_topics)
    for call_args in mock_llm_service.generate_chapter_content.call_args_list:
        topic_arg = call_args.kwargs['topic']
        # Verify that the generated content (mocked) would contain the topic
        assert any(topic_arg in topic for topic in detailed_topics)

    # Verify chapter creation and content (mocked)
    assert mock_chapter_repo.create.call_count == len(detailed_topics)
    # The mock_chapter_repo.create.side_effect ensures the returned mock chapter has the content.
    # We need to retrieve the actual created chapters to assert their content.
    # This requires a bit more advanced mocking if we want to store and retrieve them.
    # For now, we rely on the side_effect to ensure content is passed to chapter creation.
    # A more robust test would involve iterating through the call_args of mock_chapter_repo.create
    # and asserting the 'content' argument for each call.
    for i, call_args in enumerate(mock_chapter_repo.create.call_args_list):
        created_chapter_data = call_args.args[1]  # chapter_create_data is the second argument
        expected_topic = detailed_topics[i]
        assert expected_topic in created_chapter_data.content


@pytest.mark.asyncio
async def test_customization_acceptance_scenario(mocker):
    """
    Given a user selects "Academic" style and "University" level,
    When they generate a textbook,
    Then the system produces content with appropriate academic tone and university-level complexity,
    and also respects font size and layout preferences.
    """
    # Mock LLMService methods
    mock_llm_service = MagicMock()
    mock_llm_service.generate_chapter_content = AsyncMock(return_value={
        "content": "This chapter is written in an academic tone for university students, with large font and spacious layout in mind.",
        "sections": [{"title": "Section 1", "content": "Content of section 1"}]
    })
    mock_llm_service.validate_content_coherence = AsyncMock(return_value=[])
    mock_llm_service.validate_content_accuracy = AsyncMock(return_value=[])

    mocker.patch('backend.services.textbook_generation.LLMService', return_value=mock_llm_service)

    # Mock database session and repositories
    mock_db = MagicMock()
    mock_textbook_repo = MagicMock()
    mock_chapter_repo = MagicMock()
    mock_section_repo = MagicMock()

    # Mock repository create methods to return a mock object with an id
    mock_textbook_repo.create.return_value = MagicMock(id="test_textbook_id_custom")
    mock_chapter_repo.create.return_value = MagicMock(id="test_chapter_id_custom")
    mock_section_repo.create.return_value = MagicMock(id="test_section_id_custom")

    # Mock the get method of textbook_repo to return the created textbook when update is called
    mock_textbook_repo.get.side_effect = [
        MagicMock(id="test_textbook_id_custom", status=TextbookStatus.GENERATING),
        MagicMock(id="test_textbook_id_custom", status=TextbookStatus.COMPLETED)
    ]

    # For chapter creation, simulate a created chapter with a content property
    def mock_chapter_create_custom(db, chapter_create_data):
        mock_chapter = MagicMock(spec=ChapterCreate)
        mock_chapter.id = str(uuid.uuid4())
        mock_chapter.content = chapter_create_data.content
        return mock_chapter

    mock_chapter_repo.create.side_effect = mock_chapter_create_custom

    mocker.patch('backend.services.textbook_generation.TextbookRepository', mock_textbook_repo)
    mocker.patch('backend.services.textbook_generation.ChapterRepository', mock_chapter_repo)
    mocker.patch('backend.services.textbook_generation.SectionRepository', mock_section_repo)

    # Instantiate the service
    service = TextbookGenerationService(db=mock_db)

    # Create a request with customization preferences
    request = GenerateTextbookRequest(
        subject_area="Philosophy",
        target_audience="University",
        chapter_topics=["Epistemology"],
        style_preferences=StylePreferences(
            include_exercises=True,
            include_summaries=True,
            include_diagrams=False
        ),
        format_preferences=FormatPreferences(
            font_size="large",
            layout="spacious"
        )
    )

    # Call the service
    result = await service.generate_textbook(request)

    # Assertions
    assert result["textbook_id"] == "test_textbook_id_custom"
    assert result["status"] == "success"

    # Verify that generate_chapter_content was called with the correct parameters
    mock_llm_service.generate_chapter_content.assert_called_once_with(
        topic="Epistemology",
        subject_area="Philosophy",
        target_audience="University",
        include_exercises=True,
        include_summaries=True,
        include_diagrams=False,
        format_preferences={"font_size": "large", "layout": "spacious"}
    )
    # Verify that validate_content_coherence and validate_content_accuracy were called
    mock_llm_service.validate_content_coherence.assert_called_once()
    mock_llm_service.validate_content_accuracy.assert_called_once()

    # Verify chapter creation
    assert mock_chapter_repo.create.call_count == 1
    # Check the content of the created chapter (mocked content)
    created_chapter_data = mock_chapter_repo.create.call_args[0][1]
    assert "academic tone for university students" in created_chapter_data.content
    assert "large font" in created_chapter_data.content
    assert "spacious layout" in created_chapter_data.content


