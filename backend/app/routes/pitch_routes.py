from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from nodes.pitch.pitch_nodes import sales_pitch_node
from app.schemas.research_schema import PitchGenerateRequest


router = APIRouter(
    prefix="/api/pitch",
    tags=["Sales Pitch Studio"],
)


@router.post("/generate")
def generate_sales_pitch(req: PitchGenerateRequest):
    if not req.company_name or not req.prospect_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name and prospect_url are required",
        )

    state_input = {
        "company_name": req.company_name,
        "website_url": req.website_url or "",
        "prospect_url": req.prospect_url,
        "prospect_data": req.prospect_data or "",
        "website_data": f"Company: {req.company_name}, Website: {req.website_url}",
    }

    try:
        res = sales_pitch_node(state_input)
        return {
            "company_name": req.company_name,
            "prospect_url": req.prospect_url,
            "prospect_data": res.get("prospect_data", ""),
            "sales_pitch_content": res.get("sales_pitch_content", ""),
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)},
        )
