export interface ResearchResponse {
  thread_id?: string;
  company_name: string;
  website_url?: string;
  report: string;

  news_data?: {
    articles?: any[];
  };

  website_data?: {
    website_content?: string;
  };

  wikipedia_data?: {
    error?: string;
  };

  youtube_data?: {
    channel?: {
      channel_id?: string;
      title?: string;
    };

    comments?: any[];
    recent_videos?: any[];
    video_stats?: any[];
  };

  competitors_data?: string;
  competitor_matrix?: string;
  linkedin_data?: string;
  instagram_data?: string;
  twitter_data?: string;
  pr_content?: string;
  sales_pitch_content?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  type: "text" | "research_report";
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface ChatSessionSummary {
  thread_id: string;
  company_name: string;
  website_url: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatSessionDetail extends ChatSessionSummary {
  research_data?: ResearchResponse;
  messages: ChatMessage[];
}