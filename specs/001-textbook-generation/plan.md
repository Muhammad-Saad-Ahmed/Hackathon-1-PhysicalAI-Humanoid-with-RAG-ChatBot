# Implementation Plan: Textbook Generation and RAG Chatbot

**Branch**: `001-textbook-generation` | **Date**: 2025-12-09 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-textbook-generation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-native textbook generation system with integrated RAG chatbot for "Sentient Syllabus" project focused on Physical AI & Humanoid Robotics. The system will generate structured textbooks based on user specifications and provide an interactive chatbot for querying textbook content. The architecture includes a Docusaurus frontend for textbook presentation, FastAPI backend for generation and chat functionality, Qdrant vector store for RAG, and Neon Postgres for metadata.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend)
**Primary Dependencies**: FastAPI, Docusaurus, Qdrant, sentence-transformers, Neon Postgres
**Storage**: Neon Postgres for metadata, Qdrant for vector storage, GitHub Pages for static content
**Testing**: pytest (backend), Jest/Cypress (frontend)
**Target Platform**: Web application (frontend on GitHub Pages, backend on Render)
**Project Type**: Web application (frontend/backend architecture)
**Performance Goals**: <500ms response time for chat queries, <10min generation time for 10-chapter textbook
**Constraints**: Free-tier compatible, lightweight embeddings, <512MB memory usage on Render
**Scale/Scope**: Supports up to 100 textbooks with 1000s of pages each, 10k concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution:
1. ✅ Library-first: Each component (textbook generation, RAG, chat) will be implemented as separate, testable modules
2. ✅ CLI Interface: Backend will expose functionality via REST API with JSON I/O protocol
3. ✅ Test-First: TDD approach will be used with contract tests for API endpoints
4. ✅ Integration Testing: Focus on testing the integration between textbook generation, vector store, and chat functionality
5. ✅ Observability: Structured logging will be implemented for debugging and monitoring

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-contract.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure
backend/
├── main.py
├── models/
│   ├── textbook.py
│   ├── chapter.py
│   ├── section.py
│   ├── chat.py
│   └── generation_params.py
├── services/
│   ├── textbook_generation.py
│   ├── rag_service.py
│   ├── content_indexing.py
│   └── llm_service.py
├── database/
│   ├── models.py
│   ├── database.py
│   └── repositories.py
├── vector_store/
│   ├── qdrant_client.py
│   └── embedding_service.py
├── api/
│   ├── v1/
│   │   ├── textbook_router.py
│   │   ├── chat_router.py
│   │   └── index_router.py
│   └── dependencies.py
├── config/
│   └── settings.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
└── .env.example

frontend/
├── docusaurus.config.js
├── sidebars.js
├── package.json
├── docs/
│   ├── intro.md
│   ├── chapter-1.md
│   ├── chapter-2.md
│   ├── chapter-3.md
│   ├── chapter-4.md
│   ├── chapter-5.md
│   └── chapter-6.md
├── src/
│   ├── components/
│   │   ├── ChatWidget/
│   │   ├── TextbookNavigator/
│   │   ├── PersonalizeButton/
│   │   └── TranslateButton/
│   ├── pages/
│   ├── css/
│   └── theme/
├── static/
└── .env.example
```

**Structure Decision**: Web application architecture selected with separate frontend (Docusaurus) and backend (FastAPI) to enable independent scaling and development. The frontend handles textbook presentation and user interaction, while the backend manages textbook generation, RAG functionality, and data persistence.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple services (FastAPI + Qdrant + Neon) | RAG functionality requires specialized vector store and metadata database | Single database insufficient for semantic search requirements |
| Two separate deployments (GitHub Pages + Render) | Static content delivery vs. dynamic API processing have different requirements | Single deployment would compromise performance or cost-efficiency |
