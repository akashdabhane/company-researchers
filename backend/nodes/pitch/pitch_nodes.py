from graph.state import CompanyState
from lib.llm import llm
from tools.website.website_tools import search_web_via_firecrawl


def sales_pitch_node(state: CompanyState):
    company_name = state.get("company_name", "Our Company")
    website_data = str(state.get("website_data", ""))[:3000]
    prospect_url = state.get("prospect_url", "")
    prospect_data = state.get("prospect_data", "")

    # Perform web research on prospect if prospect_data is empty
    if prospect_url and not prospect_data:
        try:
            search_res = search_web_via_firecrawl.invoke({"query": f"company profile {prospect_url}", "limit": 3})
            prospect_data = str(search_res)[:2000]
        except Exception as e:
            print(f"Prospect research fallback: {e}")
            prospect_data = f"Target Prospect URL: {prospect_url}"

    prompt = f"""
    You are an elite B2B Enterprise Sales Strategist and Outreach Director.
    Create a highly personalized, high-converting Sales Prospecting Package for '{company_name}' pitching to a target prospect.

    User's Company ({company_name}) Context:
    {website_data}

    Target Prospect Info:
    Prospect URL / Identifier: {prospect_url or 'Target Enterprise Prospect'}
    Prospect Research Summary: {prospect_data or 'Enterprise customer looking for innovative automation solutions'}

    Instructions:
    Generate a complete Markdown Sales Outreach Kit with the following sections:
    
    1. 🎯 **Prospect Pain Point & ROI Match Analysis**
       - Identified business challenges for the prospect
       - How {company_name}'s product uniquely solves these pain points
    
    2. ✉️ **Personalized Cold Email Sequence**
       - **Email 1 (Initial Outreach)**: Catchy Subject Line, Personal Hook, Concise Value Prop, Soft CTA
       - **Email 2 (Follow-Up / Social Proof)**: Case study snippet / metric, quick bump CTA
    
    3. 💼 **LinkedIn Connection & DM Pitch Sequence**
       - Short, non-spammy Connection Request Note (<300 chars)
       - Follow-up DM after connection acceptance
    
    4. 🛡️ **Sales Call Objection Handling Battlecard**
       - Top 3 potential objections (e.g. Price, Competitor Switch, Implementation Time)
       - Winning response script for each objection

    Format cleanly in professional Github Markdown.
    """

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        return {
            "prospect_data": str(prospect_data),
            "sales_pitch_content": content,
        }
    except Exception as e:
        print(f"Sales Pitch Node Error: {e}")
        return {
            "prospect_data": str(prospect_data),
            "sales_pitch_content": f"### Sales Prospecting Kit for {company_name}\n\nFailed to generate automated pitch: {e}"
        }
