# 🚀 Autonomous AI Company Researcher & Business Intelligence Platform

An enterprise-grade, full-stack multi-agent business intelligence web application powered by **FastAPI**, **LangGraph**, **Google Gemini / LangChain**, **Next.js 16**, and **Tailwind CSS**.

This platform orchestrates autonomous AI research agents to gather multi-channel market intelligence on any company, building synthesized executive reports, competitor SWOT battlecards, PR & social media campaigns, tailored sales pitches, and providing an interactive conversational AI business analyst with real-time Server-Sent Events (SSE) response streaming.

---

## ✨ Features

- 🤖 **Autonomous LangGraph Multi-Agent Engine**: Supervisor-guided execution routing dedicated nodes for website parsing, Wikipedia profile extractions, YouTube analytics, media coverage, and social media listening.
- ⚡ **Real-Time Streaming Responses (SSE)**:
  - **Research Pipeline**: Streamed node-by-node progress status events as agents work.
  - **Conversational Analyst**: Live token-by-token streaming response generation for follow-up chat Q&A.
- 📊 **Synthesized Executive Intelligence Hub**:
  - **Executive Report**: Comprehensive market breakdown, strategy, and executive overview.
  - **Competitors & SWOT Battlecard**: Structured competitor matrix cards and strategic battlecard.
  - **PR & Social Studio**: Instant PR release generation and narrative theme refinement.
  - **Sales Pitch Studio**: Prospect targeting and custom sales pitch generation.
  - **Social Listening Channels**: Dedicated insights for LinkedIn, Instagram, and Twitter / X.
- 💬 **Interactive Chat Analyst**: Context-aware ChatGPT-style assistant retaining full research memory to answer follow-up questions, draft outreach emails, and refine strategy.
- 🔒 **User Session Persistence & Auth**: Integrated with Supabase Auth and a PostgreSQL/SQLite persistent database store for managing session threads and message histories.
- 🎨 **Modern Responsive UI**: Next.js 16 App Router, Tailwind CSS, Lucide icons, Dark/Light theme toggle, and GitHub Flavored Markdown rendering.

---

## 🛠️ Technology Stack

### **Backend**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Agent Orchestration**: [LangGraph](https://graph.langchain.com/) & [LangChain](https://www.langchain.com/)
- **LLM Provider**: Google Gemini (via `langchain-google-genai`) / Ollama support
- **Web Crawling & Search**: Firecrawl, NewsAPI, Wikipedia, Youtube Transcript API
- **Database & Persistence**: SQLAlchemy, PostgreSQL / SQLite

### **Frontend**
- **Framework**: [Next.js 16](https://nextjs.org/) (React 19, App Router)
- **Styling**: Vanilla CSS tokens & [Tailwind CSS v4](https://tailwindcss.com/)
- **Authentication**: [@supabase/supabase-js](https://supabase.com/)
- **Icons & Formatting**: Lucide React, React Markdown, Remark GFM, Sonner Toasts
- **Data Fetching**: Axios & EventSource SSE stream reader

---

## 📁 Repository Structure

```
company-researchers/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI Application Entry & CORS configuration
│   │   ├── database/                # SQLAlchemy database models & session setup
│   │   ├── routes/                  # API routes (research, chat, pr, pitch)
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   └── services/                # Database ChatStore service
│   ├── graph/                       # LangGraph state & compiled agent graph
│   ├── lib/                         # LLM & Firecrawl API client wrappers
│   ├── nodes/                       # Research agent nodes (website, youtube, news, social, report)
│   ├── tools/                       # Tool integrations (Firecrawl, search, web APIs)
│   └── requirements.txt             # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── app/                     # Next.js App Router pages (login, page.tsx)
    │   ├── components/              # UI components (ReportTabs, Sidebar, ChatMessages, Form)
    │   ├── lib/                     # API helpers, SSE stream readers, Supabase client
    │   └── providers/               # Authentication state provider
    ├── package.json                 # Frontend dependencies & scripts
    └── tsconfig.json                # TypeScript configuration
```

---

## 📡 API Endpoints & Streaming Architecture

| Method | Endpoint | Description | Response Format |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/research` | Run complete multi-agent research pipeline (static). | JSON (`ResearchResponse`) |
| `POST` | `/api/research-stream` | Stream real-time node execution status & final response. | `text/event-stream` (SSE) |
| `GET` | `/api/chats` | List all research chat threads for the user. | JSON array |
| `GET` | `/api/chats/{thread_id}` | Get research thread details & full chat history. | JSON (`ChatSessionDetail`) |
| `POST` | `/api/chats/{thread_id}/message` | Send follow-up chat message to AI analyst (static). | JSON |
| `POST` | `/api/chats/{thread_id}/message/stream` | Stream follow-up chat message tokens in real-time. | `text/event-stream` (SSE) |
| `DELETE`| `/api/chats/{thread_id}` | Delete research conversation thread. | JSON |
| `POST` | `/api/pr/generate` | Generate PR announcement copy. | JSON |
| `POST` | `/api/pr/refine` | Refine PR announcement based on human feedback. | JSON |
| `POST` | `/api/pitch/generate` | Generate custom sales pitch for prospect URL. | JSON |

---

## ⚙️ Environment Variables Setup

### **1. Backend Environment Variables (`backend/.env`)**
Create a `.env` file in the `backend/` directory:

```env
# Google Gemini LLM API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Firecrawl Web Scraping & Search API Key
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# News API Key (Optional for news coverage)
NEWS_API_KEY=your_news_api_key_here

# Database URL (Optional: Defaults to SQLite if omitted)
DATABASE_URL=postgresql://user:password@localhost:5432/company_researcher
```

### **2. Frontend Environment Variables (`frontend/.env`)**
Create a `.env` file in the `frontend/` directory:

```env
# Backend API Base URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Supabase Auth Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## 🚀 Getting Started

### **Prerequisites**
- Python `3.10+` installed
- Node.js `18+` and `npm` installed

---

### **1. Running the Backend (FastAPI)**

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv myvenv

# Activate the virtual environment
# Windows:
myvenv\Scripts\activate
# macOS/Linux:
source myvenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```
The backend API server will be available at **`http://localhost:8000`** (Swagger docs at `http://localhost:8000/docs`).

---

### **2. Running the Frontend (Next.js)**

```bash
# Open a new terminal and navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Next.js development server
npm run dev
```
The web application will be live at **`http://localhost:3000`**.

---

## 📜 License

This project is released under the **MIT License**.
