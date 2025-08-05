from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from dotenv import load_dotenv
import re

load_dotenv()

class VideoPerformanceAnalyzer(BaseTool):
    """
    Analyzes the performance metrics of a specific YouTube video.
    """
    video_id: str = Field(
        ..., description="The ID of the YouTube video to analyze."
    )

    def _parse_duration(self, duration):
        """Convert ISO 8601 duration to seconds."""
        match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
        if not match:
            return 0
        
        hours = int(match.group(1)[:-1]) if match.group(1) else 0
        minutes = int(match.group(2)[:-1]) if match.group(2) else 0
        seconds = int(match.group(3)[:-1]) if match.group(3) else 0
        
        return hours * 3600 + minutes * 60 + seconds

    def run(self):
        """
        Analyzes the performance metrics of a YouTube video.
        """
        print(f"\n=== Starting Video Performance Analysis for {self.video_id} ===")
        
        try:
            # Get API key from environment
            api_key = os.getenv("YOUTUBE_API_KEY")
            if not api_key:
                print("ERROR: YouTube API key not found in environment variables")
                return json.dumps({
                    "error": "YouTube API key not configured",
                    "status": "failed"
                })

            # Initialize YouTube API client
            print("Initializing YouTube API client...")
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # Get video details
            print("Fetching video details...")
            video_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=self.video_id
            ).execute()
            
            if not video_response.get('items'):
                print(f"ERROR: No video found with ID {self.video_id}")
                return json.dumps({
                    "error": f"Video not found: {self.video_id}",
                    "status": "failed"
                })
            
            video_data = video_response['items'][0]
            title = video_data['snippet']['title']
            channel = video_data['snippet']['channelTitle']
            
            print(f"\nVideo Title: {title}")
            print(f"Channel: {channel}")
            
            # Get video statistics
            stats = video_data['statistics']
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            
            # Calculate engagement rate
            engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0
            
            # Get video duration
            duration = video_data['contentDetails']['duration']
            duration_seconds = self._parse_duration(duration)
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            
            print("\nPerformance Metrics:")
            print(f"- Views: {views:,}")
            print(f"- Likes: {likes:,}")
            print(f"- Comments: {comments:,}")
            print(f"- Engagement Rate: {engagement_rate:.2f}%")
            print(f"- Duration: {minutes} minutes {seconds} seconds")
            
            # Get comments for sentiment analysis
            print("\nFetching comments for analysis...")
            try:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=self.video_id,
                    maxResults=100,
                    textFormat='plainText'
                ).execute()
                
                comments_list = comments_response.get('items', [])
                total_comments = len(comments_list)
                
                print(f"Comment Analysis:")
                print(f"- Total Comments Analyzed: {total_comments}")
                
                # Simple sentiment analysis based on likes
                if total_comments > 0:
                    total_likes = sum(int(comment['snippet']['topLevelComment']['snippet'].get('likeCount', 0)) 
                                    for comment in comments_list)
                    avg_likes = total_likes / total_comments
                    
                    if avg_likes > 10:
                        sentiment = "Very positive"
                    elif avg_likes > 5:
                        sentiment = "Positive"
                    elif avg_likes > 2:
                        sentiment = "Neutral"
                    else:
                        sentiment = "Mixed"
                else:
                    sentiment = "No comments available"
                
                print(f"- Average Sentiment: {sentiment}")
                
            except HttpError as e:
                print(f"WARNING: Could not fetch comments: {str(e)}")
                sentiment = "Comments unavailable"
            
            print("\n=== Performance Analysis Complete ===")
            
            return json.dumps({
                "status": "success",
                "video_info": {
                    "title": title,
                    "channel": channel,
                    "performance_metrics": {
                        "views": views,
                        "likes": likes,
                        "comments": comments,
                        "engagement_rate": engagement_rate,
                        "duration": f"{minutes}m {seconds}s"
                    },
                    "comment_analysis": {
                        "total_comments": total_comments,
                        "sentiment": sentiment
                    }
                }
            })
            
        except HttpError as e:
            error_message = f"YouTube API error: {str(e)}"
            print(f"ERROR: {error_message}")
            return json.dumps({
                "error": error_message,
                "status": "failed"
            })
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            print(f"ERROR: {error_message}")
            return json.dumps({
                "error": error_message,
                "status": "failed"
            })

if __name__ == "__main__":
    # Test the tool
    tool = VideoPerformanceAnalyzer(video_id="dQw4w9WgXcQ")
    result = tool.run()
    print("\nFinal Result:")
    print(result)