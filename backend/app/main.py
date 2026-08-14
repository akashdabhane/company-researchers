from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.research_routes import router as research_router


app = FastAPI(
    title="Company Researcher API",
    description="FastAPI backend for AI Company Research Agent",
    version="1.0.0",
)

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(research_router)


@app.get("/")
def health_check():
    return {"status": "healthy"}



