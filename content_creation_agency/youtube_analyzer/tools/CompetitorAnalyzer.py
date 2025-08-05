from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

load_dotenv()

class CompetitorAnalyzer(BaseTool):
    """
    A tool that analyzes competitor channels and their content strategy.
    """
    channel_id: str = Field(
        ..., description="The YouTube channel ID to analyze"
    )
    max_competitors: int = Field(
        default=5,
        description="Maximum number of competitor channels to analyze"
    )

    def run(self):
        """
        Analyze competitor channels and their content strategy.
        """
        print("CompetitorAnalyzer - running")
        try:
            print(f"CompetitorAnalyzer: Starting analysis for channel: {self.channel_id}")
            youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            # Get channel details
            channel_response = youtube.channels().list(
                part='snippet,statistics',
                id=self.channel_id
            ).execute()
            
            if not channel_response['items']:
                return "Channel not found"
                
            channel_data = channel_response['items'][0]
            channel_title = channel_data['snippet']['title']
            
            # Search for similar channels
            search_response = youtube.search().list(
                q=channel_title,
                part='snippet',
                type='channel',
                maxResults=self.max_competitors
            ).execute()
            
            competitors = []
            for item in search_response.get('items', []):
                competitor_id = item['id']['channelId']
                if competitor_id != self.channel_id:  # Skip the original channel
                    # Get competitor channel details
                    competitor_response = youtube.channels().list(
                        part='snippet,statistics,contentDetails',
                        id=competitor_id
                    ).execute()
                    
                    if competitor_response['items']:
                        competitor_data = competitor_response['items'][0]
                        
                        # Get recent videos
                        playlist_id = competitor_data['contentDetails']['relatedPlaylists']['uploads']
                        playlist_response = youtube.playlistItems().list(
                            part='snippet',
                            playlistId=playlist_id,
                            maxResults=5
                        ).execute()
                        
                        recent_videos = []
                        for video_item in playlist_response.get('items', []):
                            video_id = video_item['snippet']['resourceId']['videoId']
                            video_response = youtube.videos().list(
                                part='statistics,contentDetails',
                                id=video_id
                            ).execute()
                            
                            if video_response['items']:
                                video_data = video_response['items'][0]
                                recent_videos.append({
                                    'title': video_item['snippet']['title'],
                                    'published_at': video_item['snippet']['publishedAt'],
                                    'views': video_data['statistics'].get('viewCount', '0'),
                                    'likes': video_data['statistics'].get('likeCount', '0'),
                                    'duration': video_data['contentDetails']['duration']
                                })
                        
                        competitors.append({
                            'channel_info': {
                                'id': competitor_id,
                                'title': competitor_data['snippet']['title'],
                                'description': competitor_data['snippet']['description'],
                                'subscriber_count': competitor_data['statistics']['subscriberCount'],
                                'video_count': competitor_data['statistics']['videoCount'],
                                'view_count': competitor_data['statistics']['viewCount']
                            },
                            'recent_videos': recent_videos,
                            'content_strategy': self._analyze_content_strategy(recent_videos)
                        })
            
            analysis = {
                'target_channel': {
                    'id': self.channel_id,
                    'title': channel_title,
                    'subscriber_count': channel_data['statistics']['subscriberCount']
                },
                'competitors': competitors,
                'market_analysis': self._analyze_market_position(competitors, channel_data['statistics'])
            }
            
            print(f"CompetitorAnalyzer: Successfully analyzed {len(competitors)} competitors")
            return json.dumps(analysis)
            
        except Exception as e:
            print(f"CompetitorAnalyzer: Error analyzing competitors: {str(e)}")
            return f"Error analyzing competitors: {str(e)}"
    
    def _analyze_content_strategy(self, videos):
        """Analyze content strategy based on recent videos"""
        if not videos:
            return "No recent videos found"
        
        # Calculate average video length
        total_duration = 0
        for video in videos:
            duration = self._parse_duration(video['duration'])
            total_duration += duration
        
        avg_duration = total_duration / len(videos)
        
        # Analyze upload frequency
        dates = [datetime.fromisoformat(v['published_at'].replace('Z', '+00:00')) for v in videos]
        dates.sort()
        if len(dates) > 1:
            avg_days_between = (dates[-1] - dates[0]).days / (len(dates) - 1)
        else:
            avg_days_between = 0
        
        return {
            'average_video_length': f"{avg_duration/60:.1f} minutes",
            'upload_frequency': f"{avg_days_between:.1f} days between uploads",
            'content_types': self._identify_content_types(videos)
        }
    
    def _analyze_market_position(self, competitors, target_stats):
        """Analyze market position relative to competitors"""
        if not competitors:
            return "No competitors found"
        
        target_subs = int(target_stats['subscriberCount'])
        competitor_subs = [int(c['channel_info']['subscriber_count']) for c in competitors]
        
        avg_competitor_subs = sum(competitor_subs) / len(competitor_subs)
        market_position = "leader" if target_subs > avg_competitor_subs else "follower"
        
        return {
            'market_position': market_position,
            'subscriber_comparison': {
                'target': target_subs,
                'average_competitor': avg_competitor_subs,
                'difference_percentage': f"{((target_subs - avg_competitor_subs) / avg_competitor_subs * 100):.1f}%"
            }
        }
    
    def _parse_duration(self, duration):
        """Convert ISO 8601 duration to seconds"""
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return 0
        hours, minutes, seconds = match.groups()
        return (int(hours or 0) * 3600 + 
                int(minutes or 0) * 60 + 
                int(seconds or 0))
    
    def _identify_content_types(self, videos):
        """Identify common content types based on video titles"""
        content_types = set()
        for video in videos:
            title = video['title'].lower()
            if 'tutorial' in title or 'how to' in title:
                content_types.add('tutorials')
            if 'review' in title:
                content_types.add('reviews')
            if 'news' in title or 'update' in title:
                content_types.add('news')
            if 'vlog' in title or 'day in the life' in title:
                content_types.add('vlogs')
        
        return list(content_types) if content_types else ['general content']

if __name__ == "__main__":
    # Test the tool
    analyzer = CompetitorAnalyzer(
        channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers channel
    )
    print(analyzer.run()) 