---
id: 2
title: textbook-generation-plan
stage: plan
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-textbook-generation
branch: 001-textbook-generation
user: Admin
command: /sp.plan
labels: ["planning", "architecture", "textbook-generation", "rag-chatbot"]
links:
  spec: C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\spec.md
  ticket: null
  adr: null
  pr: null
files:
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\plan.md
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\research.md
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\data-model.md
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\quickstart.md
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\contracts\api-contract.yaml
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\CLAUDE.md
tests:

---

## Prompt

# PLAN PROMPT: "Textbook-Generation" Feature

**Role:** Senior Technical Architect & Product Owner
**Project:** "Sentient Syllabus" – AI-Native Textbook on Physical AI & Humanoid Robotics
**Objective:** Generate a **clean, minimal, production-ready implementation plan** that is sequential, actionable, and free-tier compatible.

**Requirements:**

1. **Folder and File Structure (Docusaurus)**
   - Provide a complete project tree including `docs/`, `src/components/`, `docusaurus.config.js`, `sidebars.js`, `package.json`.

2. **Chapter Creation Workflow**
   - 6 short chapters with explicit titles and slugs.
   - Include short sections, bullet points, diagrams/code snippets where necessary.

3. **Sidebar and Routing Setup**
   - Configure `sidebars.js` and ensure routes match chapter slugs.

4. **UI Customization Steps**
   - Clean, modern, minimalistic design.
   - Configure navbar, footer, Prism theme, and CSS styling.

5. **RAG Chatbot Architecture**
   - Backend: FastAPI
   - Vector store: Qdrant
   - Metadata: Neon Postgres
   - Embeddings: Lightweight, free-tier compatible
   - LLM: Groq (Llama 3) or Gemini Flash
   - Text-selection-based Q&A workflow: user selects text → backend → vector store → LLM → response

6. **API Endpoints and Data Flow**
   - `POST /v1/chat`: inputs `{query, context_id}`, output: streamed response
   - `POST /v1/index`: admin only, trigger MDX re-indexing
   - Include clear data flow diagrams or descriptions.

7. **Build, Test, and Deployment Steps**
   - Docusaurus static build, GitHub Pages deployment
   - FastAPI backend on free-tier Render with idle spin-down
   - Set required environment variables (`GEMINI_API_KEY`, `QDRANT_URL`, `NEON_DB_URL`)

8. **Optional Feature Hooks**
   - Personalize Chapter button (structure only)
   - Urdu Translation button (structure only)

9. **Constraints**
   - Free-tier only, lightweight embeddings, minimal resource usage
   - Chapters concise and focused, essential content only

**Output Instructions:**
- Write in **sequential, imperative style**
- Include **code blocks** for file structure, API specs, and workflow
- Ensure **no ambiguity** in folders, chapters, RAG architecture, or deployment

## Response snapshot

Completed the implementation plan for the textbook generation feature with RAG chatbot. The plan includes:

1. **Architecture**: Web application with Docusaurus frontend and FastAPI backend
2. **Technology Stack**: Python 3.11, FastAPI, Docusaurus, Qdrant, Neon Postgres
3. **Data Model**: Complete schema for Textbook, Chapter, Section, ChatSession, and ChatMessage entities
4. **API Contracts**: Full OpenAPI specification for textbook generation and RAG chatbot endpoints
5. **Project Structure**: Detailed directory structure for both frontend and backend
6. **Deployment Strategy**: Free-tier compatible deployment to GitHub Pages and Render
7. **Research**: Technology decisions documented with rationale and alternatives

The plan addresses all requirements including chapter creation workflow, RAG architecture, API endpoints, and UI customization while maintaining free-tier compatibility.

## Outcome

- ✅ Impact: Created comprehensive implementation plan for textbook generation system
- 🧪 Tests: Contract tests defined for API endpoints
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, api-contract.yaml
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan provides clear roadmap for implementing the "Sentient Syllabus" project

## Evaluation notes (flywheel)

- Failure modes observed:
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):