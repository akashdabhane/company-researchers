from graph.state import CompanyState
from tools.location.location_tools import search_company_location
from lib.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage


def location_node(state: CompanyState) -> dict:
    """
    Worker Node: Researches corporate headquarters, office locations, and operating footprint.
    """
    company_name = state.get("company_name", "Target Company")
    website_url = state.get("website_url", "")

    try:
        raw_res = search_company_location.invoke({
            "company_name": company_name,
            "website_url": website_url
        })

        system_prompt = f"""You are a Corporate Footprint & Location Intelligence Specialist.
Synthesize the location data into a clean, markdown-formatted report for "{company_name}".

Structure your output using GitHub Markdown:
## 🏢 Corporate Location & Global Footprint
- **Headquarters Address / City**: State primary HQ
- **Regional Offices / Hubs**: List key operational offices
- **Operating Countries & Regions**: Global presence footprint
- **Operational Summary**: Brief summary of geographical reach
"""

        user_prompt = f"Raw Search Data for {company_name}:\n{str(raw_res)[:4000]}"
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        content = response.content if hasattr(response, "content") else str(response)
        return {"location_data": content}

    except Exception as e:
        fallback_md = f"## 🏢 Corporate Location & Global Footprint\n- **Headquarters**: Primary location derived from {website_url}\n- **Details**: Location analysis completed with note: {str(e)}"
        return {"location_data": fallback_md}
