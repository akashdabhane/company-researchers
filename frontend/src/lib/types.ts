export interface ResearchResponse {
  company_name: string;
  report: string;

  news_data: {
    articles: any[];
  };

  website_data: {
    website_content: string;
  };

  wikipedia_data: {
    error?: string;
  };

  youtube_data: {
    channel?: {
      channel_id: string;
      title: string;
    };

    comments: any[];
    recent_videos: any[];
    video_stats: any[];
  };
}