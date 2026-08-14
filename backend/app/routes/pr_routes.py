from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from nodes.pr.pr_nodes import pr_copywriter_node
from app.schemas.research_schema import PRGenerateRequest, PRRefineRequest


router = APIRouter(
    prefix="/api/pr",
    tags=["PR & Social Studio"],
)


@router.post("/generate")
def generate_pr_content(req: PRGenerateRequest):
    if not req.company_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name is required",
        )

    state_input = {
        "company_name": req.company_name,
        "website_url": req.website_url or "",
        "platform": req.platform,
        "narrative_theme": req.narrative_theme,
        "human_feedback": req.human_feedback or "",
        "website_data": f"Company: {req.company_name}, Website: {req.website_url}",
        "news_data": "",
    }

    try:
        res = pr_copywriter_node(state_input)
        return {
            "company_name": req.company_name,
            "platform": req.platform,
            "narrative_theme": req.narrative_theme,
            "pr_content": res.get("pr_content", ""),
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )


@router.post("/refine")
def refine_pr_content(req: PRRefineRequest):
    if not req.company_name or not req.human_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name and human_feedback are required",
        )

    state_input = {
        "company_name": req.company_name,
        "platform": req.platform,
        "narrative_theme": req.narrative_theme,
        "human_feedback": req.human_feedback,
        "website_data": f"Current Draft:\n{req.current_content}",
        "news_data": "",
    }

    try:
        res = pr_copywriter_node(state_input)
        return {
            "company_name": req.company_name,
            "platform": req.platform,
            "narrative_theme": req.narrative_theme,
            "pr_content": res.get("pr_content", ""),
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )
