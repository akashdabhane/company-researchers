from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
import json
from graph.graph import graph
from app.schemas.research_schema import ResearchRequest, ResearchStreamRequest


router = APIRouter(
    prefix="/api",
    tags=["Research"],
)


@router.post("/research")
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
            "competitors_data": result.get("competitors_data"),
            "competitor_matrix": result.get("competitor_matrix"),
            "pr_content": result.get("pr_content"),
            "sales_pitch_content": result.get("sales_pitch_content"),
            "report": report_content,
        }

        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )



@router.post("/research-stream")
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


