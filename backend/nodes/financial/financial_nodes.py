from graph.state import CompanyState
from tools.financial.financial_tools import search_financial_info
from lib.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage


def financial_node(state: CompanyState) -> dict:
    """
    Worker Node: Analyzes financial metrics, funding rounds, revenue model, and pricing structure.
    """
    company_name = state.get("company_name", "Target Company")
    website_url = state.get("website_url", "")

    try:
        raw_res = search_financial_info.invoke({
            "company_name": company_name,
            "website_url": website_url
        })

        system_prompt = f"""You are a Venture Capital & Financial Business Analyst.
Synthesize the financial and market valuation intelligence into a markdown summary for "{company_name}".

Structure your output using GitHub Markdown:
## 💰 Financials, Funding & Revenue Model
- **Estimated Funding / Capital Raised**: Funding history or investment stage
- **Key Investors & Backers**: Notable VCs or institutional backers
- **Monetization & Pricing Model**: Business model (SaaS, Freemium, Enterprise, Tiered)
- **Market Valuation & Growth Signals**: Revenue signals or headcount expansion
- **Strategic Takeaways**: Commercial viability evaluation
"""

        user_prompt = f"Raw Financial Data for {company_name}:\n{str(raw_res)[:4000]}"
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        content = response.content if hasattr(response, "content") else str(response)
        return {"financial_data": content}

    except Exception as e:
        fallback_md = f"## 💰 Financials, Funding & Revenue Model\n- **Monetization Model**: Commercial model for {company_name} ({website_url})\n- **Details**: Financial analysis completed with note: {str(e)}"
        return {"financial_data": fallback_md}
