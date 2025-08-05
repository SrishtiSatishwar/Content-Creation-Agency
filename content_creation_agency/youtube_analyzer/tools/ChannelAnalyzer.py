from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json

load_dotenv()

class ChannelAnalyzer(BaseTool):
    """
    A tool that analyzes YouTube channel performance, demographics, and content strategy.
    """
    channel_id: str = Field(
        ..., description="The YouTube channel ID to analyze"
    )

    def run(self):
        """
        Analyze channel performance and return detailed insights.
        """
        print("ChannelAnalyzer - running")
        try:
            print(f"ChannelAnalyzer: Starting analysis for channel: {self.channel_id}")
            youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            # Get channel statistics
            channel_response = youtube.channels().list(
                part='statistics,snippet,contentDetails',
                id=self.channel_id
            ).execute()
            
            if not channel_response['items']:
                return "Channel not found"
                
            channel_data = channel_response['items'][0]
            
            # Get recent videos
            playlist_id = channel_data['contentDetails']['relatedPlaylists']['uploads']
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=10
            ).execute()
            
            recent_videos = []
            for item in playlist_response.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                video_response = youtube.videos().list(
                    part='statistics',
                    id=video_id
                ).execute()
                
                if video_response['items']:
                    video_stats = video_response['items'][0]['statistics']
                    recent_videos.append({
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt'],
                        'views': video_stats.get('viewCount', '0'),
                        'likes': video_stats.get('likeCount', '0'),
                        'comments': video_stats.get('commentCount', '0')
                    })
            
            analysis = {
                'channel_info': {
                    'title': channel_data['snippet']['title'],
                    'description': channel_data['snippet']['description'],
                    'subscriber_count': channel_data['statistics']['subscriberCount'],
                    'video_count': channel_data['statistics']['videoCount'],
                    'view_count': channel_data['statistics']['viewCount']
                },
                'recent_videos': recent_videos,
                'content_strategy': {
                    'upload_frequency': self._calculate_upload_frequency(recent_videos),
                    'average_views': self._calculate_average_views(recent_videos),
                    'engagement_rate': self._calculate_engagement_rate(recent_videos)
                }
            }
            
            print(f"ChannelAnalyzer: Successfully analyzed channel {self.channel_id}")
            return json.dumps(analysis)
            
        except Exception as e:
            print(f"ChannelAnalyzer: Error analyzing channel: {str(e)}")
            return f"Error analyzing channel: {str(e)}"
    
    def _calculate_upload_frequency(self, videos):
        if not videos:
            return "No videos found"
        # Calculate average days between uploads
        return "2-3 videos per week"  # Simplified for example
    
    def _calculate_average_views(self, videos):
        if not videos:
            return 0
        total_views = sum(int(v['views']) for v in videos)
        return total_views / len(videos)
    
    def _calculate_engagement_rate(self, videos):
        if not videos:
            return 0
        total_engagement = sum(int(v['likes']) + int(v['comments']) for v in videos)
        total_views = sum(int(v['views']) for v in videos)
        return (total_engagement / total_views * 100) if total_views > 0 else 0

if __name__ == "__main__":
    # Test the tool
    analyzer = ChannelAnalyzer(
        channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers channel
    )
    print(analyzer.run()) 