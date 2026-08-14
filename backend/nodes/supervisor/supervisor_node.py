import json
from graph.state import CompanyState
from lib.llm import llm

AVAILABLE_AGENTS = [
    "website",
    "wikipedia",
    "youtube",
    "news",
    "linkedin",
    "instagram",
    "twitter",
    "competitor",
    "report",
    "pr_copywriter",
    "sales_pitch",
    "FINISH"
]

MAX_STEPS = 8

def supervisor_node(state: CompanyState):
    company_name = state.get("company_name", "Unknown Company")
    website_url = state.get("website_url", "")
    completed_agents = state.get("completed_agents") or []
    step_count = state.get("step_count", 0) + 1

    # Check termination guards
    if step_count > MAX_STEPS:
        print(f"[SUPERVISOR] Max steps reached ({step_count}/{MAX_STEPS}). Routing to FINISH.")
        return {
            "next_agent": "FINISH",
            "supervisor_reasoning": "Maximum hop limit reached. Completing graph execution.",
            "step_count": step_count
        }

    # If final_report, pr_content, and sales_pitch_content are generated, finish
    if state.get("final_report") and state.get("pr_content") and state.get("sales_pitch_content"):
        print("[SUPERVISOR] Core reports and content generated. Routing to FINISH.")
        return {
            "next_agent": "FINISH",
            "supervisor_reasoning": "All key reports generated successfully.",
            "step_count": step_count
        }

    # If report is generated but pr_copywriter or sales_pitch haven't run, pick them next
    if state.get("final_report"):
        if "pr_copywriter" not in completed_agents:
            return {
                "next_agent": "pr_copywriter",
                "supervisor_reasoning": "Report complete; generating PR content draft.",
                "step_count": step_count
            }
        elif "sales_pitch" not in completed_agents:
            return {
                "next_agent": "sales_pitch",
                "supervisor_reasoning": "Report complete; generating Sales Pitch kit.",
                "step_count": step_count
            }
        else:
            return {
                "next_agent": "FINISH",
                "supervisor_reasoning": "All post-report tasks completed.",
                "step_count": step_count
            }

    # Assess collected data status
    data_status = {
        "website_data": bool(state.get("website_data")),
        "wikipedia_data": bool(state.get("wikipedia_data")),
        "youtube_data": bool(state.get("youtube_data")),
        "news_data": bool(state.get("news_data")),
        "linkedin_data": bool(state.get("linkedin_data")),
        "instagram_data": bool(state.get("instagram_data")),
        "twitter_data": bool(state.get("twitter_data")),
        "competitors_data": bool(state.get("competitors_data")),
    }

    # Build prompt for LLM Orchestrator decision
    prompt = f"""
You are the Executive AI Supervisor Orchestrator managing a team of specialized company research agents.

Target Company: "{company_name}"
Official Website: "{website_url}"

Execution History & Status:
- Current Hop/Step: {step_count}/{MAX_STEPS}
- Completed Agents: {completed_agents}
- Collected Intelligence:
  * Website Crawl Data: {"Collected" if data_status["website_data"] else "Missing"}
  * Wikipedia Data: {"Collected" if data_status["wikipedia_data"] else "Missing"}
  * YouTube Data: {"Collected" if data_status["youtube_data"] else "Missing"}
  * News Articles: {"Collected" if data_status["news_data"] else "Missing"}
  * LinkedIn Data: {"Collected" if data_status["linkedin_data"] else "Missing"}
  * Instagram Data: {"Collected" if data_status["instagram_data"] else "Missing"}
  * Twitter / X Data: {"Collected" if data_status["twitter_data"] else "Missing"}
  * Competitor Analysis: {"Collected" if data_status["competitors_data"] else "Missing"}

Your Task:
Decide the SINGLE NEXT sub-agent to invoke to gather research or synthesize results.

Rules:
1. Do NOT re-invoke an agent that is already in Completed Agents ({completed_agents}).
2. Priority 1: Gather primary web research ("website") if website data is missing.
3. Priority 2: Gather key channels ("wikipedia", "youtube", "news", "competitor") if relevant data is missing.
4. Priority 3: Once adequate research data has been gathered (at least 2-3 primary sources like website, wikipedia, news, or competitors), route to "report" to synthesize the executive report.
5. If enough information is gathered or if all primary agents have run, route to "report".

Valid options for next_agent MUST be one of:
["website", "wikipedia", "youtube", "news", "linkedin", "instagram", "twitter", "competitor", "report", "pr_copywriter", "sales_pitch", "FINISH"]

Respond strictly in JSON format with no extra markdown backticks:
{{
    "reasoning": "Brief explanation of why this agent was chosen",
    "next_agent": "selected_agent_name"
}}
"""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        # Clean JSON string
        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        if clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
        clean_content = clean_content.strip()

        parsed = json.loads(clean_content)
        chosen_agent = parsed.get("next_agent", "").strip().lower()
        reasoning = parsed.get("reasoning", "Supervisor routing decision.")

        # Fallback validation
        if chosen_agent not in AVAILABLE_AGENTS or chosen_agent in completed_agents:
            # Fallback heuristic logic if LLM chooses invalid/completed agent
            if "website" not in completed_agents:
                chosen_agent = "website"
            elif "news" not in completed_agents:
                chosen_agent = "news"
            elif "competitor" not in completed_agents:
                chosen_agent = "competitor"
            elif "wikipedia" not in completed_agents:
                chosen_agent = "wikipedia"
            else:
                chosen_agent = "report"

        print(f"[SUPERVISOR] Next step selected: '{chosen_agent}'. Reason: {reasoning}")

        return {
            "next_agent": chosen_agent,
            "supervisor_reasoning": reasoning,
            "step_count": step_count
        }

    except Exception as e:
        print(f"[SUPERVISOR] Parsing fallback due to: {e}")
        # Heuristic fallback
        fallback_agent = "website" if "website" not in completed_agents else "report"
        return {
            "next_agent": fallback_agent,
            "supervisor_reasoning": f"Fallback routing to {fallback_agent} due to orchestrator parse issue.",
            "step_count": step_count
        }
