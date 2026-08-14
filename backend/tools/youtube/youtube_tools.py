from langchain_core.tools import tool
from dotenv import load_dotenv
from googleapiclient.errors import HttpError
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime
from lib.youtube_client import youtube_client


load_dotenv()


@tool
def get_channel_info_by_id(channel_id: str) -> dict:
    """
    Get YouTube channel statistics and info given a channel ID.
    Returns subscriber count, view count, video count, title, description.
    """
    response = youtube_client.channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()

    item = response["items"][0]
    return {
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "subscribers": item["statistics"].get("subscriberCount"),
        "total_views": item["statistics"].get("viewCount"),
        "video_count": item["statistics"].get("videoCount"),
    }


@tool
def search_channel_by_name(company_name: str) -> dict:
    """
    Search for a YouTube channel by company or creator name.
    Returns the channel ID and title of the best match.
    """
    response = youtube_client.search().list(
        part="snippet",
        q=company_name,
        type="channel",
        maxResults=1
    ).execute()

    item = response["items"][0]
    return {
        "channel_id": item["snippet"]["channelId"],
        "title": item["snippet"]["title"],
        # "description": item["snippet"]["description"],
        # "subscribers": item["statistics"].get("subscriberCount"),
        # "total_views": item["statistics"].get("viewCount"),
        # "video_count": item["statistics"].get("videoCount"),
    }


@tool
def get_channel_by_handle(handle: str) -> dict:   # ← added : str -> dict
    """
    Get YouTube channel information by its handle (e.g., @GoogleDeepMind).
    Returns channel ID, title, description, and statistics.
    """
    response = youtube_client.channels().list(
        part="snippet,statistics,brandingSettings",
        forHandle=handle.replace("@", "")
    ).execute()

    if not response["items"]:
        return {}                                  # ← return {} instead of None
    
    item = response["items"][0]
    return {
        "channel_id": item["id"],
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "subscribers": item["statistics"].get("subscriberCount"),
        "total_views": item["statistics"].get("viewCount"),
    }


@tool
def get_recent_videos(channel_id: str, max_results: int = 10) -> list:
    """
    Get the most recent videos from a YouTube channel.
    Returns a list of video titles, IDs, and publish dates.
    """
    response = youtube_client.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    ).execute()

    return [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "description": item["snippet"]["description"][:300],
        }
        for item in response["items"]
    ]


@tool
def get_video_stats(video_id: str) -> dict:
    """
    Get engagement statistics for a specific YouTube video.
    Returns view count, like count, and comment count.
    """
    response = youtube_client.videos().list(
        part="statistics,snippet",
        id=video_id
    ).execute()

    item = response["items"][0]
    return {
        "title": item["snippet"]["title"],
        "views": item["statistics"].get("viewCount"),
        "likes": item["statistics"].get("likeCount"),
        "comments": item["statistics"].get("commentCount"),
    }


@tool
def get_video_comments(video_id: str, max_results: int = 100) -> list:  # ← added types
    """
    Get top comments for a specific YouTube video.
    Returns a list of comments with author, text, and like count.
    """

    try:
        response = youtube_client.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order="relevance"
        ).execute()

        return [
            {
                "author": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                "text": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                "likes": item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
            }
            for item in response["items"]       # ← also fixed the list bug from your ChatGPT convo
        ]

    except Exception as e:
        print(f"Error fetching comments for video {video_id}: {e}")

    except HttpError as e:
        if e.resp.status == 403:
            print(f"Comments disabled for {video_id}")
            return []
        raise


@tool
def search_channel_videos(
    channel_id: str,
    keyword: str
) -> list:
    """
    Search for videos within a specific channel using a keyword.
    Returns a list of matching videos with their IDs and titles.
    Accepts a channel ID and a search keyword, and returns videos from that channel that match the keyword in their title or description.
    """

    response = youtube_client.search().list(
        part="snippet",
        channelId=channel_id,
        q=keyword,
        maxResults=20,
        type="video"
    ).execute()

    return [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"]
        }
        for item in response["items"]
    ]




@tool
def compare_channels(channel_ids: list[str]):
    """
    Compare multiple YouTube channels by their IDs.
    Returns a list of channel info dictionaries for each channel ID provided.
    """

    data = []

    for channel_id in channel_ids:

        info = get_channel_info_by_id.invoke(channel_id)

        data.append(info)

    return data



@tool
def extract_channel_topics(channel_id: str):
    """
    Extract common topics from a channel's recent video titles.
    Returns a list of the most frequent words in the video titles.
    """

    videos = get_recent_videos.invoke({"channel_id": channel_id, "max_results": 50})

    corpus = [v["title"] for v in videos]

    vectorizer = CountVectorizer(stop_words="english")

    X = vectorizer.fit_transform(corpus)

    freq = X.sum(axis=0)

    words = vectorizer.get_feature_names_out()

    scores = [(words[i], freq[0, i]) for i in range(len(words))]

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:20]



@tool
def get_channel_playlists(channel_id: str) -> list:
    """
    Get all playlists for a given YouTube channel.
    Returns a list of playlist titles and IDs.
    """

    response = youtube_client.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50
    ).execute()

    return [
        {
            "title": item["snippet"]["title"],
            "playlist_id": item["id"]
        }
        for item in response["items"]
    ]



@tool
def get_trending_videos(region_code: str = "IN"):
    """
    Get trending videos in a specific region.
    Returns a list of trending video titles and their view counts.
    Accepts a region code (e.g., 'US', 'IN') and returns the most popular videos in that region, along with their view counts.
    """

    response = (
        youtube_client.videos()
        .list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=25,
        )
        .execute()
    )

    return [
        {
            "title": item["snippet"]["title"],
            "views": item["statistics"].get("viewCount"),
        }
        for item in response["items"]
    ]


@tool
def analyze_upload_frequency(channel_id: str):
    """
    Analyze how frequently a channel uploads videos.
    Accepts a channel ID and calculates the average number of uploads per week based on the publish dates of recent videos.
    Returns the average number of uploads per week based on the publish dates of recent videos.
    """

    videos = get_recent_videos.invoke({"channel_id": channel_id, "max_results": 50})

    dates = [
        datetime.fromisoformat(v["published_at"].replace("Z", "+00:00")) for v in videos
    ]

    if len(dates) < 2:
        return "Not enough videos"

    span = (max(dates) - min(dates)).days

    uploads_per_week = (len(dates) / max(span, 1)) * 7

    return {
        "videos_analyzed": len(dates),
        "uploads_per_week": round(uploads_per_week, 2),
    }


@tool
def get_top_performing_videos(channel_id: str):
    """
    Get the top performing videos of a channel based on view count.
    Accepts a channel ID and returns the top 10 videos sorted by view count, including their titles and view counts.

    """

    videos = get_recent_videos.invoke({"channel_id": channel_id, "max_results": 50})

    enriched = []

    for v in videos:

        stats = get_video_stats.invoke(v["video_id"])

        enriched.append({**v, **stats})

    enriched.sort(key=lambda x: int(x["views"]), reverse=True)

    return enriched[:10]




from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

@tool
def get_comment_sentiment(
    video_id: str
):
    """
    Analyze the sentiment of comments on a YouTube video.
    Returns the percentage of positive, negative, and neutral comments.
    Accepts a video ID and analyzes the sentiment of the comments, returning the percentage of positive, negative, and neutral comments based on the compound score from VADER sentiment analysis.
    """

    comments = get_video_comments.invoke(
        {
            "video_id": video_id,
            "max_results": 100
        }
    )

    positive = 0
    negative = 0
    neutral = 0

    for c in comments:

        score = analyzer.polarity_scores(
            c["text"]
        )

        compound = score["compound"]

        if compound >= 0.05:
            positive += 1
        elif compound <= -0.05:
            negative += 1
        else:
            neutral += 1

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }



from youtube_transcript_api import YouTubeTranscriptApi

@tool
def get_video_transcript(video_id: str) -> str:
    """
    Get transcript/captions from a YouTube video.
    Useful for answering content-based questions.
    Accepts a video ID and returns the transcript text, which can be used for content analysis or question answering. 
    """

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = " ".join(
        chunk["text"]
        for chunk in transcript
    )

    return text[:30000]



@tool
def summarize_video(video_id: str) -> str:
    """
    Generate a summary of a YouTube video based on its transcript.
    Accepts a video ID and returns a summarized version of the transcript.
    """

    transcript = get_video_transcript.invoke(video_id)

    return transcript[:10000]



