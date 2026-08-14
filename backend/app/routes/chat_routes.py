from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.chat_store import chat_store
from lib.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


router = APIRouter(
    prefix="/api/chats",
    tags=["Chats & Conversations"],
)


class SendMessageRequest(BaseModel):
    message: str


@router.get("")
def list_chats(x_user_id: str = Header(default="anonymous", alias="x-user-id")):
    return chat_store.get_all_chats(user_id=x_user_id)


@router.get("/{thread_id}")
def get_chat(thread_id: str, x_user_id: str = Header(default="anonymous", alias="x-user-id")):
    chat = chat_store.get_chat(user_id=x_user_id, thread_id=thread_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat thread '{thread_id}' not found",
        )
    return chat


@router.post("/{thread_id}/message")
def send_chat_message(
    thread_id: str,
    req: SendMessageRequest,
    x_user_id: str = Header(default="anonymous", alias="x-user-id")
):
    chat = chat_store.get_chat(user_id=x_user_id, thread_id=thread_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat thread '{thread_id}' not found",
        )

    user_text = req.message.strip()
    if not user_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty",
        )

    # Add user message to store
    user_msg = chat_store.add_message(
        user_id=x_user_id,
        thread_id=thread_id,
        role="user",
        content=user_text,
        msg_type="text"
    )

    # Build context for LLM
    company_name = chat.get("company_name", "Unknown Company")
    website_url = chat.get("website_url", "")
    research_data = chat.get("research_data") or {}

    system_prompt = f"""You are an elite AI Business Analyst & Company Researcher assistant.
You are in an ongoing chat session providing intelligence and follow-up analysis for the company: "{company_name}" ({website_url}).

Here is the stored research context available for {company_name}:
---
COMPANY REPORT SUMMARY:
{research_data.get('report', 'No report available.')}

COMPETITOR ANALYSIS & MATRIX:
{research_data.get('competitor_matrix', 'No competitor matrix available.')}

NEWS SUMMARY / HEADLINES:
{str(research_data.get('news_data', ''))[:1000]}

PR CONTENT DRAFT:
{research_data.get('pr_content', '')}

SALES PITCH CONTENT:
{research_data.get('sales_pitch_content', '')}
---

Your Task:
- Answer the user's follow-up questions accurately, professionally, and concisely using the research context above.
- If requested to draft PR copy, social media posts, competitor comparisons, or sales pitches, provide well-formatted GitHub Markdown output.
- Be direct, helpful, and maintain context across the conversation.
"""

    messages = [SystemMessage(content=system_prompt)]

    # Add previous chat history
    for m in chat.get("messages", [])[:-1]:  # exclude the user message just added
        if m["type"] == "research_report":
            messages.append(AIMessage(content=f"Initial Executive Report for {company_name} is generated and ready."))
        elif m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            messages.append(AIMessage(content=m["content"]))

    # Add current user message
    messages.append(HumanMessage(content=user_text))

    try:
        response = llm.invoke(messages)
        ai_content = response.content if hasattr(response, "content") else str(response)

        ai_msg = chat_store.add_message(
            user_id=x_user_id,
            thread_id=thread_id,
            role="assistant",
            content=ai_content,
            msg_type="text"
        )

        return {
            "user_message": user_msg,
            "assistant_message": ai_msg,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating AI response: {str(e)}",
        )


@router.delete("/{thread_id}")
def delete_chat(thread_id: str, x_user_id: str = Header(default="anonymous", alias="x-user-id")):
    success = chat_store.delete_chat(user_id=x_user_id, thread_id=thread_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat thread '{thread_id}' not found",
        )
    return {"status": "deleted", "thread_id": thread_id}
