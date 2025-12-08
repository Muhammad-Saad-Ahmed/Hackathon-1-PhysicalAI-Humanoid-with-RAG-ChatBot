# Quickstart Guide: Textbook Generation and RAG Chatbot

## Project Overview

This project implements an AI-native textbook generation system with an integrated RAG (Retrieval Augmented Generation) chatbot. The system allows educators to generate custom textbooks and enables students to ask questions about the content through an interactive chat interface.

## Prerequisites

- Node.js 18+ (for Docusaurus frontend)
- Python 3.9+ (for FastAPI backend)
- Git
- Access to Gemini API (free tier)
- Access to Render for deployment (free tier)

## Local Development Setup

### Frontend (Docusaurus)

1. **Clone and install dependencies**:
```bash
cd frontend
npm install
```

2. **Set environment variables**:
```bash
cp .env.example .env
# Edit .env with your API endpoints and keys
```

3. **Run development server**:
```bash
npm start
```

### Backend (FastAPI)

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys and service URLs
```

4. **Run the server**:
```bash
uvicorn main:app --reload
```

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_GEMINI_API_KEY=your_gemini_api_key
```

### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DB_URL=your_neon_postgres_connection_string
SECRET_KEY=your_secret_key
```

## API Endpoints

### Textbook Generation
- `POST /v1/textbooks` - Generate a new textbook
- `GET /v1/textbooks/{id}` - Get textbook details

### RAG Chatbot
- `POST /v1/chat` - Query the chatbot
- `POST /v1/index` - Admin endpoint to re-index content

## Key Components

### Frontend Structure
```
frontend/
├── docs/                 # Textbook content in MDX format
├── src/
│   ├── components/       # React components for textbook UI
│   ├── pages/            # Additional pages
│   └── theme/            # Custom Docusaurus theme components
├── docusaurus.config.js  # Docusaurus configuration
└── sidebars.js           # Navigation sidebar configuration
```

### Backend Structure
```
backend/
├── main.py              # FastAPI application entry point
├── models/              # Pydantic models for API contracts
├── services/            # Business logic for textbook generation and RAG
├── database/            # Database models and operations
├── vector_store/        # Qdrant integration for RAG
└── api/                 # API route definitions
```

## Running Tests

### Frontend
```bash
npm test
npm run build
```

### Backend
```bash
pytest
```

## Deployment

### Frontend to GitHub Pages
1. Update `docusaurus.config.js` with your deployment settings
2. Run: `npm run deploy`

### Backend to Render
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variables in Render dashboard
4. Deploy automatically on push to main branch

## Troubleshooting

1. **Frontend build errors**: Ensure Node.js version is 18+
2. **Backend connection errors**: Check environment variables and service availability
3. **API rate limits**: Verify your Gemini API quota hasn't been exceeded
4. **Vector search issues**: Ensure Qdrant collection is properly indexed