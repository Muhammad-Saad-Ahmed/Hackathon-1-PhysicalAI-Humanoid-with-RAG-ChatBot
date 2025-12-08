# Data Model: Textbook Generation Feature

## Core Entities

### Textbook
- **id**: UUID (primary key)
- **title**: String (required)
- **subject_area**: String (required) - e.g., "Physical AI", "Humanoid Robotics"
- **target_audience**: String (required) - e.g., "High School", "University", "Professional"
- **description**: Text (optional)
- **created_at**: DateTime (required)
- **updated_at**: DateTime (required)
- **status**: Enum ["draft", "generating", "completed", "failed"] (required)
- **generation_params**: JSON (required) - serialized generation parameters
- **export_formats**: Array[String] - available export formats ["PDF", "ePub", "MDX"]
- **relationships**:
  - chapters (one-to-many with Chapter)

### Chapter
- **id**: UUID (primary key)
- **textbook_id**: UUID (foreign key to Textbook)
- **title**: String (required)
- **slug**: String (required) - URL-friendly version of title
- **content**: Text (required) - the chapter content in MDX format
- **position**: Integer (required) - order in textbook
- **word_count**: Integer (optional)
- **reading_time**: Integer (optional) - estimated in minutes
- **created_at**: DateTime (required)
- **updated_at**: DateTime (required)
- **relationships**:
  - textbook (many-to-one with Textbook)
  - sections (one-to-many with Section)

### Section
- **id**: UUID (primary key)
- **chapter_id**: UUID (foreign key to Chapter)
- **title**: String (required)
- **content**: Text (required)
- **position**: Integer (required) - order in chapter
- **section_type**: Enum ["text", "code", "diagram", "exercise", "summary"] (required)
- **created_at**: DateTime (required)
- **updated_at**: DateTime (required)
- **relationships**:
  - chapter (many-to-one with Chapter)

### GenerationParameter
- **id**: UUID (primary key)
- **name**: String (required) - e.g., "subject_area", "target_audience"
- **value**: String (required)
- **textbook_id**: UUID (foreign key to Textbook, optional)
- **created_at**: DateTime (required)
- **relationships**:
  - textbook (many-to-one with Textbook, optional)

### ChatSession
- **id**: UUID (primary key)
- **textbook_id**: UUID (foreign key to Textbook, optional)
- **chapter_id**: UUID (foreign key to Chapter, optional)
- **created_at**: DateTime (required)
- **updated_at**: DateTime (required)
- **relationships**:
  - messages (one-to-many with ChatMessage)

### ChatMessage
- **id**: UUID (primary key)
- **session_id**: UUID (foreign key to ChatSession)
- **role**: Enum ["user", "assistant"] (required)
- **content**: Text (required)
- **context_snippet**: Text (optional) - the selected text that triggered the question
- **created_at**: DateTime (required)
- **relationships**:
  - session (many-to-one with ChatSession)

## Vector Store Schema (Qdrant)

### TextbookContent Collection
- **payload**:
  - content_id: UUID - references either Chapter.id or Section.id
  - content_type: String - "chapter" or "section"
  - textbook_id: UUID - references Textbook.id
  - chapter_id: UUID - references Chapter.id (if content_type is "section")
  - text: String - the actual content to be embedded
  - metadata: JSON - additional information like headings, context
- **vector**: Float array - embedding vector from sentence-transformers

## API Contract Models

### Request/Response Objects

#### GenerateTextbookRequest
- **subject_area**: String (required)
- **target_audience**: String (required)
- **chapter_topics**: Array[String] (required)
- **style_preferences**: Object (optional)
  - include_exercises: Boolean
  - include_summaries: Boolean
  - include_diagrams: Boolean
- **format_preferences**: Object (optional)
  - font_size: String
  - layout: String

#### GenerateTextbookResponse
- **textbook_id**: UUID (required)
- **status**: String (required) - "success", "queued", "error"
- **estimated_completion**: Integer (optional) - seconds

#### ChatQueryRequest
- **query**: String (required)
- **context_id**: String (optional) - could be chapter_id or section_id
- **session_id**: String (optional) - for maintaining conversation context

#### ChatQueryResponse
- **response**: String (required)
- **sources**: Array[Object] (optional)
  - content_id: String
  - title: String
  - relevance_score: Float

## Database Relationships

```
Textbook (1) ←→ (M) Chapter
Chapter (1) ←→ (M) Section
Textbook (1) ←→ (M) GenerationParameter
Textbook (1) ←→ (M) ChatSession
Chapter (1) ←→ (M) ChatSession
ChatSession (1) ←→ (M) ChatMessage
```

## Indexes

- Textbook: created_at, status
- Chapter: textbook_id, position
- Section: chapter_id, position
- ChatMessage: session_id, created_at