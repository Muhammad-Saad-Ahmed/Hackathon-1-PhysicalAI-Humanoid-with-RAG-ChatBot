<!-- 
Sync Impact Report:
Version change: N/A → 1.0.0
Added sections: Core Principles (6 principles), Architecture Requirements, Content Validation, Success Criteria
Removed sections: None
Templates requiring updates: ⚠ pending (.specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### I. Simplicity Over Complexity
All design decisions MUST prioritize simplicity without sacrificing functionality. Systems must be minimal, structured, and correct. Features that add complexity without clear value are prohibited. This principle applies to code architecture, user interfaces, and learning content.

### II. Content Integrity and Accuracy
All textbook content MUST remain minimal, structured, and technically accurate. Content must be verifiable and grounded in the established Physical AI & Humanoid Robotics curriculum. No hallucinated or unverifiable content is permitted. All technical statements must be correct and verifiable.

### III. Lightweight Architecture for Free-Tier Deployment
The system architecture MUST be designed for minimal compute usage and free-tier infrastructure. Components must operate efficiently without requiring GPU resources, using lightweight embeddings and processing only. This includes using Cohere's embed-multilingual-light-v3.0 for embeddings.

### IV. AI Responses Strictly Grounded in Book Text
The RAG chatbot MUST answer ONLY from the book text. No external hallucinated content is allowed. All AI responses must be verifiable against the textbook content. This ensures educational accuracy and prevents misleading information.

### V. Consistent User Experience and Formatting
All chapters and UI components MUST follow consistent writing style, formatting, and visual design. The textbook and chatbot interface MUST maintain a clean, modern, minimal aesthetic using Docusaurus v3. Chapter lengths, format, and tone MUST be consistent across all content.

### VI. Production-Safe and Fast Performance
All code and content MUST ensure fast build times, clean structure, and production-safe operation. Systems MUST be designed for deployment to GitHub Pages and FastAPI hosting. Zero ambiguity in definitions, content boundaries, and roles MUST be maintained.

## Architecture Requirements

All technical implementations MUST adhere to the specified architecture:

1. **Embeddings**: Use Cohere `embed-multilingual-light-v3.0` for vector representations
2. **Rerank (optional)**: Use Cohere `rerank-v3.0` for result refinement
3. **Chat Agent**: Use Gemini API (OpenAI-compatible) with tool routing for agent orchestration
4. **Chat UI**: Implement ChatKit React components for front-end interaction
5. **Vector Storage**: Use Qdrant (Cloud Free Tier) for semantic storage
6. **Metadata & History**: Use Neon Postgres for user state and metadata
7. **API Server**: Implement FastAPI for backend services
8. **Deployment**: Deploy Docusaurus to GitHub Pages, FastAPI to Render/Fly.io

The architecture MUST remain lightweight and operate within free-tier infrastructure constraints.

## Content Validation Rules

All textbook content MUST comply with the following validation rules:

1. **No Hallucinated Content**: All content must be based on established Physical AI & Humanoid Robotics curriculum
2. **No External Material**: Content must not include robotics material beyond the specified course scope
3. **Technical Accuracy**: All technical statements must be correct and verifiable
4. **Consistent Format**: Chapters must follow uniform length, format, and tone
5. **Essential Focus**: Explanations must be minimal and focused only on essentials

## Success Criteria

The project achieves success when ALL of the following conditions are met:

1. Constitution is internally consistent and free of contradictions
2. The book builds successfully on Docusaurus
3. RAG chatbot returns accurate answers grounded in book text
4. Architecture works on free-tier infrastructure (Cohere + Gemini + Qdrant + Neon)
5. UI is clean, modern, professional, and fast
6. Full project deploys smoothly to GitHub Pages + FastAPI hosting

## Non-Goals

The following items are explicitly OUT OF SCOPE:

1. Additional chapters or modules beyond the 6 defined
2. External datasets or robotics platforms beyond the specified scope
3. GPU-heavy model training pipelines
4. Non-Docusaurus frontends

## Scope

The textbook MUST contain exactly 6 concise chapters:

1. Introduction to Physical AI
2. Basics of Humanoid Robotics
3. ROS 2 Fundamentals
4. Lightweight Simulation (URDF + PyBullet)
5. Vision-Language-Action Systems
6. Capstone: Simple AI-Robot Pipeline

All chapters must remain concise, technically accurate, minimal, and aligned with course outcomes.

## Governance

This Constitution is the authoritative source for all project decisions and supersedes any conflicting practices or documentation. Amendments to this Constitution require explicit documentation, approval, and migration planning. All development efforts must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-01-08 | **Last Amended**: 2025-01-08