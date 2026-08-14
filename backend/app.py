import json
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn

from graph.graph import graph

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


class ResearchRequest(BaseModel):
    company_name: str
    website_url: str
    email: Optional[str] = None


class ResearchStreamRequest(BaseModel):
    company_name: str
    website_url: str


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/research")
def research_company(req: ResearchRequest):
    if not req.company_name or not req.website_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name and website_url are required",
        )

    config = {
        "configurable": {
            "thread_id": "user_123"
        }
    }

    try:
        result = graph.invoke({
            "company_name": req.company_name,
            "website_url": req.website_url
        }, config=config)

        print("Graph Result:", result)

        report_content = ""
        if (
            result.get("final_report")
            and isinstance(result["final_report"], dict)
            and "messages" in result["final_report"]
            and len(result["final_report"]["messages"]) > 0
        ):
            report_content = result["final_report"]["messages"][-1].content
        elif hasattr(result.get("final_report"), "content"):
            report_content = result["final_report"].content

        response = {
            "company_name": result.get("company_name"),
            "website_data": result.get("website_data"),
            "youtube_data": result.get("youtube_data"),
            "news_data": result.get("news_data"),
            "wikipedia_data": result.get("wikipedia_data"),
            "report": report_content,
        }

        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )


@app.post("/api/research-stream")
def research_company_stream(req: ResearchStreamRequest):
    config = {
        "configurable": {
            "thread_id": "user_123"
        }
    }

    def generate():
        try:
            for event in graph.stream(
                {
                    "company_name": req.company_name,
                    "website_url": req.website_url,
                },
                config=config,
                stream_mode="updates",
            ):
                yield f"data: {json.dumps(event)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
