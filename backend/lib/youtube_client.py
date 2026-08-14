import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import httplib2



load_dotenv()

# Disable SSL verification — only for local dev/testing, never in production
http = httplib2.Http(disable_ssl_certificate_validation=True)


youtube_client = build(
    "youtube", 
    "v3", 
    developerKey=os.getenv("YOUTUBE_API_KEY"),
    http=http
)

