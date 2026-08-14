from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import JSONResponse, StreamingResponse
import json
import uuid
from graph.graph import graph
from app.schemas.research_schema import ResearchRequest, ResearchStreamRequest
from app.services.chat_store import chat_store


router = APIRouter(
    prefix="/api",
    tags=["Research"],
)


@router.post("/research")
def research_company(
    req: ResearchRequest,
    x_user_id: str = Header(default="anonymous", alias="x-user-id")
):
    if not req.company_name or not req.website_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name and website_url are required",
        )

    thread_id = req.thread_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        result = graph.invoke({
            "company_name": req.company_name,
            "website_url": req.website_url,
            "completed_agents": [],
            "step_count": 0
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
        elif isinstance(result.get("final_report"), str):
            report_content = result["final_report"]

        response = {
            "thread_id": thread_id,
            "company_name": result.get("company_name", req.company_name),
            "website_url": result.get("website_url", req.website_url),
            "linkedin_data": result.get("linkedin_data"),
            "instagram_data": result.get("instagram_data"),
            "twitter_data": result.get("twitter_data"),
            "competitors_data": result.get("competitors_data"),
            "competitor_matrix": result.get("competitor_matrix"),
            "pr_content": result.get("pr_content"),
            "sales_pitch_content": result.get("sales_pitch_content"),
            "report": report_content,
        }

        # Store session in ChatStore for the specific user
        chat_store.create_or_update_research_session(
            user_id=x_user_id,
            thread_id=thread_id,
            company_name=req.company_name,
            website_url=req.website_url,
            research_data=response
        )

        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )



@router.post("/research-stream")
def research_company_stream(
    req: ResearchRequest,
    x_user_id: str = Header(default="anonymous", alias="x-user-id")
):
    if not req.company_name or not req.website_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name and website_url are required",
        )

    thread_id = req.thread_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    def generate():
        try:
            accumulated_state = {
                "company_name": req.company_name,
                "website_url": req.website_url,
            }

            yield f"data: {json.dumps({'type': 'status', 'node': 'init', 'message': f'Initializing research pipeline for {req.company_name}...'})}\n\n"

            for event in graph.stream(
                {
                    "company_name": req.company_name,
                    "website_url": req.website_url,
                    "completed_agents": [],
                    "step_count": 0
                },
                config=config,
                stream_mode="updates",
            ):
                # event is a dict mapping node_name -> output dict
                for node_name, output in event.items():
                    if isinstance(output, dict):
                        accumulated_state.update(output)

                    friendly_messages = {
                        "supervisor": "Supervisor agent assigning intelligence tasks...",
                        "website_scraper": "Scraping & parsing official company website data...",
                        "wikipedia": "Extracting company history & profile from Wikipedia...",
                        "youtube": "Gathering YouTube video metrics & channel insights...",
                        "news": "Retrieving latest press coverage & news articles...",
                        "social_linkedin": "Analyzing LinkedIn company profile & updates...",
                        "social_instagram": "Evaluating Instagram brand presence & content...",
                        "social_twitter": "Gathering Twitter / X social listening data...",
                        "competitors": "Analyzing industry competitors & drafting battlecard matrix...",
                        "pr": "Generating PR announcements & media press release draft...",
                        "pitch": "Building customized sales pitch & target recommendations...",
                        "report": "Synthesizing executive research report...",
                    }

                    msg = friendly_messages.get(node_name, f"Completed step: {node_name}")

                    yield f"data: {json.dumps({'type': 'status', 'node': node_name, 'message': msg})}\n\n"

            # Graph finished; extract report content
            report_content = ""
            if (
                accumulated_state.get("final_report")
                and isinstance(accumulated_state["final_report"], dict)
                and "messages" in accumulated_state["final_report"]
                and len(accumulated_state["final_report"]["messages"]) > 0
            ):
                report_content = accumulated_state["final_report"]["messages"][-1].content
            elif hasattr(accumulated_state.get("final_report"), "content"):
                report_content = accumulated_state["final_report"].content
            elif isinstance(accumulated_state.get("final_report"), str):
                report_content = accumulated_state["final_report"]

            response = {
                "thread_id": thread_id,
                "company_name": accumulated_state.get("company_name", req.company_name),
                "website_url": accumulated_state.get("website_url", req.website_url),
                "linkedin_data": accumulated_state.get("linkedin_data"),
                "instagram_data": accumulated_state.get("instagram_data"),
                "twitter_data": accumulated_state.get("twitter_data"),
                "competitors_data": accumulated_state.get("competitors_data"),
                "competitor_matrix": accumulated_state.get("competitor_matrix"),
                "pr_content": accumulated_state.get("pr_content"),
                "sales_pitch_content": accumulated_state.get("sales_pitch_content"),
                "report": report_content,
            }

            # Store session in ChatStore for the user
            chat_store.create_or_update_research_session(
                user_id=x_user_id,
                thread_id=thread_id,
                company_name=req.company_name,
                website_url=req.website_url,
                research_data=response
            )

            yield f"data: {json.dumps({'type': 'complete', 'data': response})}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


