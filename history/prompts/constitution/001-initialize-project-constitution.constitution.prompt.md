---
id: 001
title: Initialize Project Constitution
stage: constitution
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Admin
command: /sp.constitution
labels: ["constitution", "initialization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ./.specify/memory/constitution.md
tests:
  - Constitution internal consistency checks
---

## Prompt

Project Name: Physical AI & Humanoid Robotics — Essentials

Task:
Generate a complete, formal Constitution for this project using the updated architecture.
The Constitution must follow Spec-Kit standards with zero ambiguity:
- Clear, structured sections
- Strict scope rules
- Defined constraints
- Content validation rules
- Constitution validation rules
- Alignment with Cohere + Gemini API + ChatKit + Qdrant + Neon architecture

Purpose:
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course.
The book must serve as a fast, minimal, high-quality learning resource and pair perfectly with an integrated RAG chatbot powered by:
- Cohere embeddings + rerank
- Gemini API (OpenAI-compatible) for agent orchestration and chat/completions
- ChatKit React components for UI
- FastAPI backend tools
- Qdrant vector database
- Neon Postgres metadata + user state

Scope:
The textbook contains exactly 6 concise chapters:
1. Introduction to Physical AI
2. Basics of Humanoid Robotics
3. ROS 2 Fundamentals
4. Lightweight Simulation (URDF + PyBullet)
5. Vision-Language-Action Systems
6. Capstone: Simple AI-Robot Pipeline

All chapters must remain concise, technically accurate, minimal, and aligned with course outcomes.
The UI must be clean, modern, minimal, and built on Docusaurus v3.

Core Principles:
- Simplicity over complexity
- Content must remain minimal, structured, and correct
- Lightweight architecture designed for free-tier compute
- Cohere used for embeddings, reranking, and optional generation
- Gemini API + ChatKit used for agent orchestration and frontend chat UI
- RAG chatbot must answer ONLY from book text
- Consistent writing style and formatting across all chapters
- Fast build, clean structure, and production-safe code
- Zero ambiguity in definitions, content boundaries, and roles

Key Features:
- Docusaurus-based AI-Native textbook
- Integrated RAG chatbot using:
  - Cohere embeddings + rerank
  - Qdrant vector database
  - Neon Postgres metadata + user state
  - FastAPI backend tools
  - Gemini API for agent logic + ChatKit UI
- “Select Text → Ask AI” interaction
- Ready-to-enable:
  - Urdu Translation button
  - Personalize Chapter button
  - User profile-adaptive content

Architecture Requirements:
- Embeddings: Cohere `embed-multilingual-light-v3.0`
- Rerank (optional): Cohere `rerank-v3.0`
- Chat Agent: Gemini API (OpenAI-compatible) with tool routing
- Chat UI: ChatKit React components
- Vector Storage: Qdrant (Cloud Free Tier)
- Metadata + history: Neon Postgres
- API Server: FastAPI
- Deployment: Docusaurus → GitHub Pages, FastAPI → Render/Fly.io

Constraints:
- Minimal compute usage
- No GPU required
- Lightweight embeddings only
- Chapters must remain short
- No external hallucinated content
- All AI answers must be grounded strictly in the book

Non-Goals:
- No additional chapters or modules beyond the 6 defined
- No external datasets or robotics platforms beyond scope
- No GPU-heavy model training pipelines
- No non-Docusaurus frontends

Success Criteria:
- Constitution is internally consistent and free of contradictions
- The book builds successfully on Docusaurus
- RAG chatbot returns accurate answers grounded in book text
- Architecture works on free-tier infrastructure (Cohere + Gemini + Qdrant + Neon)
- UI is clean, modern, professional, and fast
- Full project deploys smoothly to GitHub Pages + FastAPI hosting

Content Validation Rules:
- No hallucinated content
- No external robotics material beyond course scope
- All technical statements must be correct and verifiable
- Chapters must follow consistent length, format, and tone
- Explanations must be minimal and focused on essentials only

Constitution Validation Rules:
- Must reflect the exact 6-chapter structure
- Must enforce the updated AI architecture
- No unapproved concepts, chapters, or sections may be introduced
- No ambiguity or contradictory instructions
- Format must be suitable for Spec-Kit workflow: Constitution → Spec → Plan → Build
- All constraints, rules, and success criteria must align exactly with project goals

Instruction:
Using all the information above, generate the complete Constitution with:
- Clear sections
- Strong boundaries
- Strict adherence to the updated architecture
- Zero ambiguity
- Full compliance with Spec-Kit conventions

## Response snapshot

Successfully initialized the project constitution, detailing core principles, architecture, scope, and validation rules. Generated version 1.0.0. Manual follow-up required for template updates.

## Outcome

- ✅ Impact: Constitution established, providing foundational project guidance.
- 🧪 Tests: Internal consistency of constitution verified.
- 📁 Files: `./.specify/memory/constitution.md` created/modified.
- 🔁 Next prompts: Update dependent spec, plan, and task templates.
- 🧠 Reflection: Successfully translated user requirements into a formal constitution, aligning with Spec-Kit standards and specified architecture.

## Evaluation notes (flywheel)

- Failure modes observed: None observed.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
