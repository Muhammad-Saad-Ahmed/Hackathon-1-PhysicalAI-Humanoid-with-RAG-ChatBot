# Research: Textbook Generation Feature

## Research Tasks

### Technology Decisions

**Decision: Docusaurus Framework**
- **Rationale**: Docusaurus is ideal for documentation-heavy projects like textbooks, with built-in features for sidebar navigation, search, and multi-page layouts. It's React-based and supports MDX for rich content.
- **Alternatives considered**:
  - Next.js: More complex setup for documentation-focused projects
  - Gatsby: Good but heavier than needed for textbook content
  - Hugo: Static site generator but less suitable for interactive features

**Decision: FastAPI Backend**
- **Rationale**: FastAPI offers excellent performance, automatic API documentation, and strong typing. It's perfect for the RAG chatbot API endpoints.
- **Alternatives considered**:
  - Flask: Simpler but lacks modern features and performance
  - Express.js: Good but requires more setup for type safety
  - Django: Feature-rich but overkill for this use case

**Decision: Qdrant Vector Store**
- **Rationale**: Qdrant is lightweight, efficient, and offers good performance for RAG applications. It has a free tier suitable for this project.
- **Alternatives considered**:
  - Pinecone: Managed but potentially costly
  - Weaviate: Good alternative but Qdrant is more lightweight
  - ChromaDB: Local-first but may not scale well for collaborative use

**Decision: Neon Postgres for Metadata**
- **Rationale**: Neon provides serverless Postgres with built-in connection pooling and branching features. It's free-tier friendly and integrates well with FastAPI.
- **Alternatives considered**:
  - SQLite: Simpler but lacks concurrent access needed for collaborative features
  - Supabase: Good alternative but Neon is more lightweight for this use case

**Decision: LLM Provider (Groq vs Gemini Flash)**
- **Rationale**: Both offer fast inference and are cost-effective. Gemini Flash provides better context understanding for educational content. Will use Gemini Flash for its educational focus.
- **Alternatives considered**:
  - OpenAI: More expensive than free-tier compatible options
  - Anthropic: Good but potentially overkill for this use case

### Architecture Research

**Decision: Text-Selection-Based Q&A Workflow**
- **Rationale**: This provides an intuitive user experience where users can select text in the textbook and ask questions about it directly. This workflow is straightforward to implement and understand.
- **Implementation**: JavaScript event listeners capture text selection, send to backend API with context

**Decision: Chapter Structure and Content**
- **Rationale**: For the "Sentient Syllabus" project on Physical AI & Humanoid Robotics, the 6 chapters will focus on core concepts with practical applications.
- **Chapter Topics**:
  1. Introduction to Physical AI and Humanoid Robotics
  2. Kinematics and Motion Planning
  3. Perception Systems and Sensor Fusion
  4. Control Systems and Actuation
  5. Learning and Adaptation in Physical AI
  6. Ethics and Future of Humanoid Robotics

### Implementation Constraints

**Decision: Free-Tier Compatibility**
- **Rationale**: All technology choices prioritize free-tier availability to ensure the project can be deployed without cost.
- **Considerations**:
  - Qdrant Cloud has free tier with 1M vectors
  - Neon Postgres free tier with 10GB storage
  - Render free tier for FastAPI backend with 512MB RAM and 100GB transfer
  - Gemini API free tier for limited requests

**Decision: Lightweight Embeddings**
- **Rationale**: To stay within free-tier constraints and provide fast responses, using sentence-transformers/all-MiniLM-L6-v2 which is efficient but still effective for educational content.
- **Alternative**: OpenAI embeddings are more powerful but not free-tier compatible

### UI/UX Decisions

**Decision: Clean, Minimalistic Design**
- **Rationale**: Educational content should be the focus, not distracting design elements. A clean interface improves readability and learning.
- **Implementation**: Using Docusaurus default theme with custom CSS for branding

**Decision: Deployment Strategy**
- **Rationale**: Docusaurus static build to GitHub Pages for frontend, FastAPI backend on Render for RAG functionality.
- **Benefits**: Cost-effective, scalable, and leverages free-tier services