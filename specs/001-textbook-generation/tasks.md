# Implementation Tasks: Textbook Generation and RAG Chatbot

**Feature**: Textbook Generation and RAG Chatbot
**Branch**: 001-textbook-generation
**Created**: 2025-12-09
**Input**: Plan, Spec, Data Model, API Contracts

## Implementation Strategy

This project implements an AI-native textbook generation system with integrated RAG chatbot for "Sentient Syllabus" project focused on Physical AI & Humanoid Robotics. The system will generate structured textbooks based on user specifications and provide an interactive chatbot for querying textbook content.

The implementation follows a phased approach:
1. Setup phase: Initialize project structure with frontend and backend
2. Foundational phase: Implement core data models and API foundations
3. User Story phases: Implement features in priority order (P1, P2, P3)
4. Polish phase: Add cross-cutting concerns and deployment

## Dependencies

User stories can be implemented independently after the foundational phase is complete. The core data models and API foundations must be established first.

## Parallel Execution Examples

- API endpoints can be developed in parallel with frontend components
- Textbook generation service can be developed in parallel with chat service
- Database models can be implemented in parallel with vector store integration

---

## Phase 1: Setup (Project Scaffolding)

### Goal
Initialize the project structure with frontend (Docusaurus) and backend (FastAPI) components.

- [X] T001 Create root directory structure with frontend/ and backend/ subdirectories
- [X] T002 [P] Setup frontend using npx create-docusaurus@latest in frontend/ directory
- [X] T003 [P] Initialize backend virtual environment and create requirements.txt with fastapi, uvicorn, groq, fastembed, qdrant-client, neon-client, sentence-transformers
- [X] T004 Create docker-compose.yml for local development with services for backend, frontend, and Qdrant
- [X] T005 [P] Create initial gitignore files for both frontend and backend with appropriate entries
- [X] T006 [P] Setup initial package.json in frontend with required dependencies

---

## Phase 2: Foundational (Core Models and API Foundations)

### Goal
Implement core data models, database connections, and foundational API components that all user stories will depend on.

- [X] T007 [P] Implement Textbook model in backend/models/textbook.py based on data model specification
- [ ] T008 [P] Implement Chapter model in backend/models/chapter.py based on data model specification
- [ ] T009 [P] Implement Section model in backend/models/section.py based on data model specification
- [ ] T010 [P] Implement GenerationParameter model in backend/models/generation_params.py based on data model specification
- [ ] T011 [P] Implement ChatSession model in backend/models/chat_session.py based on data model specification
- [ ] T012 [P] Implement ChatMessage model in backend/models/chat_message.py based on data model specification
- [ ] T013 Setup database connection in backend/database/database.py using Neon Postgres
- [ ] T014 [P] Implement database repositories in backend/database/repositories.py for all models
- [ ] T015 [P] Implement Qdrant client in backend/vector_store/qdrant_client.py for vector storage
- [ ] T016 [P] Implement embedding service in backend/vector_store/embedding_service.py using sentence-transformers
- [ ] T017 [P] Create backend/config/settings.py with environment configuration
- [ ] T018 Create backend/main.py with FastAPI app initialization and basic routing
- [ ] T019 [P] Implement backend/api/dependencies.py with common dependencies like database session
- [ ] T020 [P] Setup CORS middleware in main.py for frontend integration
- [ ] T021 [P] Create backend/api/v1/base_router.py with basic API versioning setup

---

## Phase 3: User Story 1 - Generate Custom Textbook Content (Priority: P1)

### Goal
Implement the core functionality to generate textbooks based on user specifications (subject area, target audience, chapter topics).

### Independent Test Criteria
Can be fully tested by providing a subject area and target audience, and verifying that a well-structured textbook with appropriate content is generated that meets the specified requirements.

- [ ] T022 [P] [US1] Create textbook generation request/response models in backend/models/textbook_generation.py
- [ ] T023 [P] [US1] Implement textbook generation service in backend/services/textbook_generation.py
- [ ] T024 [P] [US1] Implement content generation using LLM in backend/services/llm_service.py
- [ ] T025 [P] [US1] Create textbook generation endpoint POST /v1/textbooks in backend/api/v1/textbook_router.py
- [ ] T026 [P] [US1] Implement textbook status tracking in backend/services/textbook_generation.py
- [ ] T027 [P] [US1] Create textbook retrieval endpoint GET /v1/textbooks/{textbook_id} in backend/api/v1/textbook_router.py
- [ ] T028 [P] [US1] Implement textbook content structuring in backend/services/textbook_generation.py
- [ ] T029 [P] [US1] Add progress indicators to textbook generation in backend/services/textbook_generation.py
- [ ] T030 [P] [US1] Implement content validation for coherence and pedagogical appropriateness
- [ ] T031 [P] [US1] Add quality checks for factual accuracy in generated content
- [ ] T032 [P] [US1] Implement chunking for large requests in backend/services/textbook_generation.py
- [ ] T033 [P] [US1] Create frontend component for textbook generation form in src/components/TextbookGenerator.jsx
- [ ] T034 [P] [US1] Connect frontend to backend textbook generation API
- [ ] T035 [P] [US1] Implement loading states and progress indicators in frontend
- [ ] T036 [P] [US1] Add error handling for textbook generation in frontend
- [ ] T037 [P] [US1] Create test for textbook generation acceptance scenario 1
- [ ] T038 [P] [US1] Create test for textbook generation acceptance scenario 2

---

## Phase 4: User Story 2 - Customize Textbook Format and Style (Priority: P2)

### Goal
Allow users to customize the generated textbook's format, style, and presentation to match their specific requirements.

### Independent Test Criteria
Can be tested by selecting different formatting options and verifying that the generated textbook reflects these choices in its structure and presentation.

- [ ] T039 [P] [US2] Extend textbook generation service to support format preferences
- [ ] T040 [P] [US2] Implement style preference handling in backend/services/textbook_generation.py
- [ ] T041 [P] [US2] Add format customization options to textbook generation request model
- [ ] T042 [P] [US2] Update textbook generation endpoint to handle style preferences
- [ ] T043 [P] [US2] Implement pedagogical element inclusion (exercises, summaries, diagrams)
- [ ] T044 [P] [US2] Create format customization UI component in frontend/src/components/FormatCustomizer.jsx
- [ ] T045 [P] [US2] Add customization options to textbook generation form
- [ ] T046 [P] [US2] Update backend to generate content with appropriate academic tone based on target audience
- [ ] T047 [P] [US2] Implement font size and layout preferences in content generation
- [ ] T048 [P] [US2] Add UI for including/excluding pedagogical elements
- [ ] T049 [P] [US2] Create test for customization acceptance scenario
- [ ] T050 [P] [US2] Update data model to store format preferences in GenerationParameter

---

## Phase 5: User Story 3 - Export and Share Generated Textbooks (Priority: P3)

### Goal
Enable users to export generated textbooks in various formats (PDF, ePub, etc.) and save generation parameters for future use.

### Independent Test Criteria
Can be tested by generating a textbook and successfully exporting it to multiple formats, verifying that the content is preserved appropriately in each format.

- [ ] T051 [P] [US3] Implement PDF export service in backend/services/export_service.py
- [ ] T052 [P] [US3] Implement ePub export service in backend/services/export_service.py
- [ ] T053 [P] [US3] Create export endpoint POST /v1/textbooks/{textbook_id}/export in backend/api/v1/textbook_router.py
- [ ] T054 [P] [US3] Add export formats to Textbook model and repository
- [ ] T055 [P] [US3] Implement parameter saving functionality in backend/services/parameter_service.py
- [ ] T056 [P] [US3] Create parameter retrieval endpoint in backend/api/v1/textbook_router.py
- [ ] T057 [P] [US3] Add export format preservation to export services
- [ ] T058 [P] [US3] Create export format selection UI in frontend/src/components/ExportOptions.jsx
- [ ] T059 [P] [US3] Implement export functionality in frontend
- [ ] T060 [P] [US3] Add parameter saving/loading UI to textbook generation form
- [ ] T061 [P] [US3] Create test for export acceptance scenario
- [ ] T062 [P] [US3] Update textbook model to track available export formats

---

## Phase 6: RAG Chatbot Implementation

### Goal
Implement the RAG (Retrieval Augmented Generation) chatbot functionality that allows users to ask questions about textbook content.

- [ ] T063 [P] Implement RAG service in backend/services/rag_service.py for vector search and retrieval
- [ ] T064 [P] Create chat endpoint POST /v1/chat in backend/api/v1/chat_router.py
- [ ] T065 [P] Implement content indexing service in backend/services/content_indexing.py
- [ ] T066 [P] Create indexing endpoint POST /v1/index in backend/api/v1/index_router.py
- [ ] T067 [P] Implement text chunking for vector storage in backend/services/content_indexing.py
- [ ] T068 [P] Add vector storage integration to Chapter and Section models
- [ ] T069 [P] Implement session management for chat conversations
- [ ] T070 [P] Add source attribution to chat responses
- [ ] T071 [P] Create ChatWidget component in frontend/src/components/ChatWidget.jsx
- [ ] T072 [P] Implement context menu for text selection in frontend/src/components/ContextMenu.jsx
- [ ] T073 [P] Connect frontend chat widget to backend chat API
- [ ] T074 [P] Add message history display in chat widget
- [ ] T075 [P] Implement streaming responses in backend chat endpoint
- [ ] T076 [P] Add authentication/authorization to indexing endpoint

---

## Phase 7: Frontend UI & Integration

### Goal
Complete the frontend implementation with proper navigation, styling, and integration with backend services.

- [ ] T077 [P] Update docusaurus.config.js with Linear-style theme and proper navigation
- [ ] T078 [P] Create sidebar navigation based on generated textbook structure in sidebars.js
- [ ] T079 [P] Implement textbook content display in Docusaurus docs
- [ ] T080 [P] Add Personalize Chapter button component in frontend/src/components/PersonalizeButton.jsx
- [ ] T081 [P] Add Urdu Translation button component in frontend/src/components/TranslateButton.jsx
- [ ] T082 [P] Integrate chat widget with textbook content pages
- [ ] T083 [P] Add loading states and error handling throughout frontend
- [ ] T084 [P] Implement responsive design for all components
- [ ] T085 [P] Add accessibility features to all components
- [ ] T086 [P] Create custom Docusaurus theme components for branding

---

## Phase 8: Content Structure (The Textbook)

### Goal
Create the initial content structure for the Physical AI & Humanoid Robotics textbook with 6 MDX files.

- [ ] T087 [P] Create 6 MDX files in frontend/docs/: intro.mdx, hardware.mdx, ros2.mdx, sim.mdx, vla.mdx, capstone.mdx
- [ ] T088 [P] Create static/img/ folder for textbook assets
- [ ] T089 [P] Add initial content to MDX files with appropriate structure
- [ ] T090 [P] Clean up default Docusaurus blog/docs to prepare for textbook content
- [ ] T091 [P] Create initial textbook navigation in sidebars.js
- [ ] T092 [P] Add proper headings and structure to MDX files for RAG indexing

---

## Phase 9: Testing and Quality Assurance

### Goal
Implement comprehensive testing to ensure system reliability and quality.

- [ ] T093 [P] Create unit tests for all backend services
- [ ] T094 [P] Create integration tests for API endpoints
- [ ] T095 [P] Create contract tests based on API specification
- [ ] T096 [P] Create frontend component tests
- [ ] T097 [P] Implement end-to-end tests for user workflows
- [ ] T098 [P] Add API request validation and error handling
- [ ] T099 [P] Implement logging and monitoring in backend
- [ ] T100 [P] Add input validation and sanitization

---

## Phase 10: Deployment (Free Tier)

### Goal
Deploy the application to production using free-tier services.

- [ ] T101 [P] Create Render deployment configuration for backend
- [ ] T102 [P] Add environment variables for Render deployment (GROQ_API_KEY, QDRANT_URL, etc.)
- [ ] T103 [P] Create GitHub Pages deployment configuration for frontend
- [ ] T104 [P] Set up GitHub Actions for automated deployment
- [ ] T105 [P] Configure health checks and monitoring
- [ ] T106 [P] Set up SSL certificates and domain configuration
- [ ] T107 [P] Document deployment process in README
- [ ] T108 [P] Perform final integration testing in deployed environment

---

## Phase 11: Polish & Cross-Cutting Concerns

### Goal
Add finishing touches and address cross-cutting concerns.

- [ ] T109 [P] Add comprehensive error handling throughout application
- [ ] T110 [P] Implement proper authentication and authorization
- [ ] T111 [P] Add rate limiting to API endpoints
- [ ] T112 [P] Optimize performance for large textbooks
- [ ] T113 [P] Add caching for frequently accessed content
- [ ] T114 [P] Implement backup and recovery procedures
- [ ] T115 [P] Add comprehensive documentation
- [ ] T116 [P] Perform security audit and vulnerability assessment
- [ ] T117 [P] Add analytics and usage tracking
- [ ] T118 [P] Finalize user interface with consistent styling
- [ ] T119 [P] Add loading states and performance indicators
- [ ] T120 [P] Create final README with setup and usage instructions