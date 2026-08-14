import json
from graph.state import CompanyState
from lib.llm import llm
from tools.competitors.competitor_tools import search_competitors_via_web


def competitor_discovery_node(state: CompanyState):
    company_name = state.get("company_name", "Unknown Company")
    website_data = state.get("website_data", "")

    # Perform web search for competitors
    search_results = []
    try:
        search_results = search_competitors_via_web.invoke(
            {"company_name": company_name}
        )
    except Exception as e:
        print(f"Error in competitor search: {e}")

    prompt = f"""
    You are an expert Competitive Intelligence Analyst.
    Your objective is to identify top competitors for '{company_name}' and produce a comprehensive Competitive Battlecard.

    Target Company Data:
    Company Name: {company_name}
    Website Data Summary: {str(website_data)[:3000]}
    Web Search Results: {str(search_results)[:2000]}

    Instructions:
    1. Identify 3 to 5 direct and indirect competitors of {company_name}.
    2. Provide detailed information for each competitor in JSON-compatible format.
    3. Generate a Markdown Competitive Battlecard containing:
       - Competitor Profiles Table
       - Feature & Positioning Comparison Matrix
       - SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats vs {company_name})
       - Strategic Positioning & Differentiators

    Return your output strictly as a JSON string with the following structure:
    {{
        "competitors": [
            {{
                "name": "Competitor Name",
                "website": "https://example.com",
                "type": "Direct" or "Indirect",
                "description": "Brief summary of competitor",
                "pricing": "Freemium / Paid / Enterprise",
                "key_advantage": "Main strength over others"
            }}
        ],
        "battlecard_markdown": "Full Markdown formatted Battlecard Matrix & SWOT analysis"
    }}
    Do not include markdown code block backticks like ```json in the wrapper if possible, or return valid JSON content.
    """

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        # Clean string if enclosed in markdown backticks
        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        if clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
        clean_content = clean_content.strip()

        parsed = json.loads(clean_content)
        competitors_list = parsed.get("competitors", [])
        battlecard_md = parsed.get("battlecard_markdown", content)

        return {
            "competitors_data": json.dumps(competitors_list),
            "competitor_matrix": battlecard_md,
        }
    except Exception as e:
        print(f"Fallback competitor parsing: {e}")
        # Fallback structured markdown
        fallback_md = f"### Competitive Intelligence for {company_name}\n\nSearch and LLM synthesis completed. Review raw analysis.\n\n{content if 'content' in locals() else str(e)}"
        return {
            "competitors_data": json.dumps([
                {
                    "name": "Market Alternatives",
                    "website": "N/A",
                    "type": "Direct",
                    "description": f"Competitors identified in {company_name}'s domain.",
                    "pricing": "Variable",
                    "key_advantage": "Established market presence"
                }
            ]),
            "competitor_matrix": fallback_md,
        }
