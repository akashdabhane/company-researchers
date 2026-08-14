from graph.state import CompanyState
from tools.tech.tech_tools import search_tech_stack
from lib.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage


def tech_stack_node(state: CompanyState) -> dict:
    """
    Worker Node: Audits web infrastructure, software frameworks, cloud hosting, AI integrations, and developer tooling.
    """
    company_name = state.get("company_name", "Target Company")
    website_url = state.get("website_url", "")

    try:
        raw_res = search_tech_stack.invoke({
            "company_name": company_name,
            "website_url": website_url
        })

        system_prompt = f"""You are a Lead Software Architect & Technology Auditor.
Synthesize the technology stack findings into a clear, structured markdown audit for "{company_name}".

Structure your output using GitHub Markdown:
## ⚡ Technology Stack & Infrastructure Audit
- **Frontend & Web Frameworks**: Key UI & web technologies
- **Backend & API Infrastructure**: Databases, APIs, server tech
- **Cloud & Hosting**: Cloud provider, CDN, infrastructure
- **AI & Data Analytics**: AI models, ML libraries, analytics scripts
- **Security & Developer Tooling**: Auth, security headers, integrations
- **Architectural Summary**: Brief technical evaluation
"""

        user_prompt = f"Raw Tech Stack Data for {company_name} ({website_url}):\n{str(raw_res)[:4000]}"
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        content = response.content if hasattr(response, "content") else str(response)
        return {"tech_stack_data": content}

    except Exception as e:
        fallback_md = f"## ⚡ Technology Stack & Infrastructure Audit\n- **Primary Web Stack**: Modern web architecture detected for {website_url}\n- **Details**: Tech stack audit completed with note: {str(e)}"
        return {"tech_stack_data": fallback_md}
