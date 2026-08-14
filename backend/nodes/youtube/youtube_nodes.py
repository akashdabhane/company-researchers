from graph.state import CompanyState
from tools.youtube.youtube_tools import (
    get_channel_info_by_id,
    search_channel_by_name,
    get_channel_by_handle,
    compare_channels,
    extract_channel_topics,
    get_channel_playlists,
    get_trending_videos,
    analyze_upload_frequency,
    get_top_performing_videos,
    get_comment_sentiment,
    get_video_transcript,
    summarize_video,
    get_recent_videos,
    get_video_stats,
    get_video_comments,
    search_channel_videos
)
from langchain_google_genai import ChatGoogleGenerativeAI   # ← only this changes
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver


def youtube_node(state: CompanyState):

    company = state["company_name"]

    channel = search_channel_by_name.invoke(company)
    recent_videos = get_recent_videos.invoke(channel["channel_id"])
    videos_stats = [get_video_stats.invoke(video['video_id']) for video in recent_videos]
    comments = [get_video_comments.invoke(video['video_id']) for video in recent_videos]

    return {
        "youtube_data": {
            "channel": channel,
            "recent_videos": recent_videos,
            "video_stats": videos_stats,
            "comments": comments
        }
    }


## youtueb agent
# 1. Define your LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    convert_system_message_to_human=True,  # ← required for Gemini
)

# 2. Register all your tools in a list
tools = [
    get_channel_info_by_id,
    search_channel_by_name,
    get_channel_by_handle,
    compare_channels,
    extract_channel_topics,
    get_channel_playlists,
    get_trending_videos,
    analyze_upload_frequency,
    get_top_performing_videos,
    get_comment_sentiment,
    get_video_transcript,
    summarize_video,
    get_recent_videos,
    get_video_stats,
    get_video_comments,
    search_channel_videos,
]


memory = MemorySaver()

# 3. Create the agent — this builds the full ReAct loop for you
youtube_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
    You are a YouTube channel research assistant.
    When given a company or creator name, you will:
    1. Find their official YouTube channel
    2. Fetch channel statistics
    3. Fetch their recent videos
    4. Summarize what the channel is about and how it performs
    5. Provide insights on the channel's content strategy and audience engagement
    6. Suggest potential improvements for the channel's growth and reach
    7. Return the information in a structured format, don't include technical details or code snippets in your response (eg. channel id, video ids, etc).
    
    if given a query or question related to a specific channel, video, playlist of any channel, you will:
    1. Identify the relevant channel, video, or playlist using the appropriate tools
    2. Fetch the necessary information or data related to the query
    3. Analyze the information and provide a comprehensive answer to the user's question based on the channel's content, statistics, and audience engagement.
    4. Return the answer in a clear and concise manner, avoiding technical jargon and code snippets in your response.

    Always use tools step by step. Never guess channel IDs.
    """,
    checkpointer=memory,
)


def youtube_node2(state):
    result = youtube_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f""" Company Name: {state["company_name"]}""",
                },
            ],
        }
    )

    content = result["youtube_data"]

    return {
        "youtube_data": content,
    }