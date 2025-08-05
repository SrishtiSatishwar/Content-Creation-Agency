from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from dotenv import load_dotenv
import time

load_dotenv()

class VideoSearcher(BaseTool):
    """
    Searches for YouTube videos based on a query and returns relevant results.
    """
    query: str = Field(
        ..., description="The search query to find relevant YouTube videos."
    )
    max_results: int = Field(
        default=5, description="Maximum number of videos to return."
    )

    def run(self):
        """
        Executes the YouTube video search and returns formatted results.
        """
        print("\n=== Starting VideoSearcher ===")
        print(f"Search Query: {self.query}")
        print(f"Max Results: {self.max_results}")

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
            
            # Execute search request
            print("Executing search request...")
            search_response = youtube.search().list(
                q=self.query,
                part='id,snippet',
                maxResults=self.max_results,
                type='video'
            ).execute()

            # Process search results
            print(f"\nFound {len(search_response.get('items', []))} videos")
            videos = []
            
            for item in search_response.get('items', []):
                try:
                    video_id = item['id']['videoId']
                    print(f"\nAnalyzing video: {video_id}")
                    
                    # Get video details
                    video_response = youtube.videos().list(
                        part='statistics,contentDetails',
                        id=video_id
                    ).execute()
                    
                    if not video_response.get('items'):
                        print(f"WARNING: No details found for video {video_id}")
                        continue
                        
                    video_data = video_response['items'][0]
                    title = item['snippet']['title']
                    channel = item['snippet']['channelTitle']
                    views = int(video_data['statistics'].get('viewCount', 0))
                    duration = video_data['contentDetails']['duration']
                    
                    print(f"Title: {title}")
                    print(f"Channel: {channel}")
                    print(f"Views: {views}")
                    print(f"Duration: {duration}")
                    
                    videos.append({
                        'video_id': video_id,
                        'title': title,
                        'channel': channel,
                        'views': views,
                        'duration': duration
                    })
                    
                except HttpError as e:
                    print(f"ERROR: YouTube API error for video {video_id}: {str(e)}")
                    continue
                except Exception as e:
                    print(f"ERROR: Unexpected error processing video {video_id}: {str(e)}")
                    continue

            if not videos:
                print("WARNING: No videos were successfully processed")
                return json.dumps({
                    "error": "No videos could be processed",
                    "status": "failed"
                })

            # Format results
            print("\n=== VideoSearcher Summary ===")
            print(f"Total videos analyzed: {len(videos)}")
            print("Video IDs for further analysis:")
            for video in videos:
                print(f"- {video['video_id']}: {video['title']}")

            return json.dumps({
                "status": "success",
                "videos": videos
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
    tool = VideoSearcher(query="neural networks basics")
    result = tool.run()
    print("\nFinal Result:")
    print(result)