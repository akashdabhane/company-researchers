from graph.state import CompanyState
from lib.llm import llm


def pr_copywriter_node(state: CompanyState):
    company_name = state.get("company_name", "Our Company")
    platform = state.get("platform", "LinkedIn")
    narrative_theme = state.get("narrative_theme", "Product Launch & Major Announcement")
    human_feedback = state.get("human_feedback", "")
    website_data = str(state.get("website_data", ""))[:3000]
    news_data = str(state.get("news_data", ""))[:1500]

    prompt = f"""
    You are an elite Brand Strategist and PR Communications Director.
    Craft a compelling, highly engaging public post or press release for '{company_name}'.

    Context & Background:
    - Company Name: {company_name}
    - Target Platform: {platform} (Format strictly according to {platform} best practices)
    - Narrative Focus / Theme: {narrative_theme}
    - Company Website Context: {website_data}
    - Recent Media / News Context: {news_data}
    """

    if human_feedback:
        prompt += f"\n- Specific User Feedback / Steering Instructions: {human_feedback}\n"
        prompt += "\nIMPORTANT: Strictly apply the user's feedback instructions above to modify tone, messaging, or structure."

    prompt += f"""

    Formatting Guidelines:
    - If LinkedIn: Professional yet human tone, compelling hook, short readable paragraphs, key takeaways, relevant hashtags, clear call to action.
    - If Twitter / X: A punchy 3 to 5 tweet thread with numbered posts (1/4, 2/4...), engaging hook, relevant emojis, viral thread style.
    - If Instagram: Engaging caption format, emoji highlights, suggested visual asset concept (e.g. [Visual Suggestion: ...]), hashtag block.
    - If Press Release: Formal corporate PR format with FOR IMMEDIATE RELEASE, DATELINE, Headline, Sub-headline, Lead Paragraph, Executive Quote, Boilerplate, and Media Contact info.

    Output only the ready-to-publish text with markdown formatting.
    """

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        return {"pr_content": content}
    except Exception as e:
        print(f"PR Copywriter Node Error: {e}")
        return {"pr_content": f"### {platform} Post Draft ({narrative_theme})\n\nFailed to generate automated copy: {e}"}
