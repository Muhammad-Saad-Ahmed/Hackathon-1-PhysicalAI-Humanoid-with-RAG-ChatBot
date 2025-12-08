---
id: 3
title: textbook-generation-tasks
stage: tasks
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-textbook-generation
branch: 001-textbook-generation
user: Admin
command: /sp.tasks
labels: ["tasks", "implementation", "textbook-generation", "rag-chatbot"]
links:
  spec: C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\spec.md
  plan: C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\plan.md
  ticket: null
  adr: null
  pr: null
files:
 - C:\Users\Admin\Downloads\Spec-Driven-Development\Book Working\New_Hackthone - (RAG)\New Working\specs\001-textbook-generation\tasks.md
tests:

---

## Prompt

# TASK PROMPT: "Textbook-Generation" Execution

**Role:** Senior Technical Architect & Project Manager
**Project:** "Sentient Syllabus" – AI-Native Textbook on Physical AI & Humanoid Robotics
**Context:** Task list MUST align 100% with the Constitution (Requirements) and Specification Document (sp.specify).

**Objective:**
Generate a granular, sequential Task Checklist to build the entire system.

**Format:**
Numbered list of actionable steps (e.g., "1.1 Initialize project...")
**Constraint:** Tasks must match the Spec Stack (e.g., use Groq, FastEmbed, FastAPI; no OpenAI).

---

## Required Task Categories

### Phase 1: Monorepo Scaffolding
1.1 Initialize root directory with `frontend/` (Docusaurus) and `backend/` (FastAPI) folders.
1.2 Setup frontend using `npx create-docusaurus@latest`.
1.3 Setup backend virtual environment and `requirements.txt` including: `fastapi`, `uvicorn`, `groq`, `fastembed`, `qdrant-client`, `neon-client`.
1.4 Create `docker-compose.yml` for local development.

---

### Phase 2: Content Structure (The Textbook)
2.1 Clean up default Docusaurus blog/docs.
2.2 Create 6 MDX files as defined in Spec:
- `docs/intro.mdx` – Physical AI
- `docs/hardware.mdx` – Humanoid Basics
- `docs/ros2.mdx` – ROS 2 Fundamentals
- `docs/sim.mdx` – Digital Twin/Gazebo
- `docs/vla.mdx` – VLA Systems
- `docs/capstone.mdx` – Pipeline Project
2.3 Create `static/img/` folder for assets.

---

### Phase 3: RAG Backend Implementation
3.1 Implement `backend/ingest.py`: parse MDX files, chunk text, embed using **FastEmbed (CPU)**, upload to **Qdrant Cloud**.
3.2 Implement `backend/server.py`:
- `POST /chat`: Receives query → Search Qdrant → Send to Groq (Llama 3) → Return stream.
3.3 Enable CORS for Docusaurus frontend URL.

---

### Phase 4: Frontend UI & Integration
4.1 Create `src/components/ChatWidget.jsx`: floating button that calls FastAPI backend.
4.2 Create `src/components/ContextMenu.jsx`: triggers on `window.getSelection()` to "Ask AI" about selected text.
4.3 Update `docusaurus.config.js`: set Linear-style theme and sidebar navigation.

---

### Phase 5: Deployment (Free Tier)
5.1 Deploy Backend to Render.com (Web Service).
- Sub-task: Add Environment Variables (`GROQ_API_KEY`, `QDRANT_URL`, etc.).
5.2 Deploy Frontend to Vercel.

---

## Output Instructions
- Review for conflicts:
  - Must use **FastEmbed**, not OpenAI.
  - Must have exactly **6 chapters**.
  - Backend must be **Python (FastAPI)**.
- Output as **Markdown Checklist** using:
```markdown
- [ ] Task...
```

## Response snapshot

Generated a comprehensive task list for implementing the textbook generation and RAG chatbot system. The tasks are organized into 11 phases:

1. Setup (project scaffolding)
2. Foundational (core models and API foundations)
3. User Story 1 (textbook generation)
4. User Story 2 (format customization)
5. User Story 3 (export functionality)
6. RAG Chatbot implementation
7. Frontend UI & integration
8. Content structure (6 MDX files)
9. Testing and quality assurance
10. Deployment
11. Polish and cross-cutting concerns

The task list includes 120 specific tasks with proper formatting including checkboxes, task IDs, user story labels where appropriate, and specific file paths. Tasks are organized by user story to enable independent implementation and testing as required by the specification.

## Outcome

- ✅ Impact: Created detailed implementation task list with 120 actionable tasks
- 🧪 Tests: Included testing tasks throughout the implementation
- 📁 Files: Created tasks.md with comprehensive task breakdown
- 🔁 Next prompts: Ready for implementation using /sp.implement
- 🧠 Reflection: Task list aligns with specification and enables incremental delivery

## Evaluation notes (flywheel)

- Failure modes observed:
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):