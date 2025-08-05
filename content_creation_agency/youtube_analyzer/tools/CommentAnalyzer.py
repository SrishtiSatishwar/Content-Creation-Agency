from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from collections import Counter

load_dotenv()

class CommentAnalyzer(BaseTool):
    """
    A tool that analyzes YouTube video comments for sentiment, engagement, and trends.
    """
    video_id: str = Field(
        ..., description="The YouTube video ID to analyze"
    )
    max_comments: int = Field(
        default=100,
        description="Maximum number of comments to analyze"
    )

    def run(self):
        """
        Analyze video comments and return insights.
        """
        print(f"\n=== Comment Analysis for Video {self.video_id} ===")
        try:
            youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
            
            video_response = youtube.videos().list(
                part='snippet,statistics',
                id=self.video_id
            ).execute()
            
            if not video_response['items']:
                print("Video not found")
                return "Video not found"
                
            video_data = video_response['items'][0]
            print(f"\nAnalyzing comments for: {video_data['snippet']['title']}")
            
            comments = []
            next_page_token = None
            
            while len(comments) < self.max_comments:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=self.video_id,
                    maxResults=min(100, self.max_comments - len(comments)),
                    pageToken=next_page_token,
                    order='relevance'
                ).execute()
                
                for item in comments_response.get('items', []):
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'likes': comment['likeCount'],
                        'published_at': comment['publishedAt'],
                        'updated_at': comment['updatedAt']
                    })
                
                next_page_token = comments_response.get('nextPageToken')
                if not next_page_token or len(comments) >= self.max_comments:
                    break
            
            print(f"\nComment Collection:")
            print(f"- Total comments collected: {len(comments)}")
            
            # Analyze comments
            engagement_metrics = self._calculate_engagement_metrics(comments)
            sentiment_analysis = self._analyze_sentiment(comments)
            common_topics = self._identify_common_topics(comments)
            comment_timeline = self._analyze_comment_timeline(comments)
            
            print("\nEngagement Metrics:")
            print(f"- Total likes: {engagement_metrics['total_likes']}")
            print(f"- Average likes per comment: {engagement_metrics['average_likes_per_comment']}")
            print(f"- Engagement rate: {engagement_metrics['engagement_rate']}")
            
            print("\nSentiment Analysis:")
            print(f"- Overall sentiment: {sentiment_analysis['overall_sentiment']}")
            print(f"- Average sentiment score: {sentiment_analysis['average_sentiment_score']}")
            print("\nSentiment Distribution:")
            for sentiment, count in sentiment_analysis['sentiment_distribution'].items():
                print(f"- {sentiment}: {count} comments")
            
            print("\nCommon Topics:")
            for topic in common_topics['top_topics'][:5]:
                print(f"- {topic['word']}: {topic['count']} occurrences")
            
            print("\nComment Timeline:")
            print(f"- First comment: {comment_timeline['first_comment']}")
            print(f"- Last comment: {comment_timeline['last_comment']}")
            print(f"- Peak activity hour: {comment_timeline['peak_hour']}")
            
            analysis = {
                'video_info': {
                    'title': video_data['snippet']['title'],
                    'view_count': video_data['statistics'].get('viewCount', '0'),
                    'like_count': video_data['statistics'].get('likeCount', '0'),
                    'comment_count': video_data['statistics'].get('commentCount', '0')
                },
                'comment_analysis': {
                    'total_comments_analyzed': len(comments),
                    'engagement_metrics': engagement_metrics,
                    'sentiment_analysis': sentiment_analysis,
                    'common_topics': common_topics,
                    'top_comments': sorted(comments, key=lambda x: x['likes'], reverse=True)[:5],
                    'comment_timeline': comment_timeline
                }
            }
            
            print("\n=== Comment Analysis Complete ===")
            return json.dumps(analysis)
            
        except Exception as e:
            print(f"Error analyzing comments: {str(e)}")
            return f"Error analyzing comments: {str(e)}"
    
    def _calculate_engagement_metrics(self, comments):
        """Calculate engagement metrics from comments"""
        if not comments:
            return "No comments found"
        
        total_likes = sum(comment['likes'] for comment in comments)
        avg_likes = total_likes / len(comments)
        
        # Calculate engagement rate (likes per comment)
        engagement_rate = total_likes / len(comments)
        
        return {
            'total_likes': total_likes,
            'average_likes_per_comment': f"{avg_likes:.1f}",
            'engagement_rate': f"{engagement_rate:.1f} likes per comment"
        }
    
    def _analyze_sentiment(self, comments):
        """Analyze comment sentiment based on likes and keywords"""
        if not comments:
            return "No comments found"
        
        # Simple sentiment analysis based on likes and keywords
        positive_keywords = {'great', 'awesome', 'amazing', 'love', 'thanks', 'thank', 'helpful', 'good'}
        negative_keywords = {'bad', 'poor', 'wrong', 'terrible', 'waste', 'boring', 'confusing'}
        
        sentiment_scores = []
        for comment in comments:
            text = comment['text'].lower()
            likes = comment['likes']
            
            # Calculate sentiment score based on keywords and likes
            score = 0
            score += sum(1 for word in positive_keywords if word in text)
            score -= sum(1 for word in negative_keywords if word in text)
            score += min(likes / 10, 2)  # Cap the like influence
            
            sentiment_scores.append(score)
        
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        if avg_sentiment > 1:
            sentiment = "Very Positive"
        elif avg_sentiment > 0:
            sentiment = "Positive"
        elif avg_sentiment > -1:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"
        
        return {
            'overall_sentiment': sentiment,
            'average_sentiment_score': f"{avg_sentiment:.1f}",
            'sentiment_distribution': {
                'very_positive': sum(1 for s in sentiment_scores if s > 1),
                'positive': sum(1 for s in sentiment_scores if 0 < s <= 1),
                'neutral': sum(1 for s in sentiment_scores if -1 <= s <= 0),
                'negative': sum(1 for s in sentiment_scores if s < -1)
            }
        }
    
    def _identify_common_topics(self, comments):
        """Identify common topics in comments"""
        if not comments:
            return "No comments found"
        
        # Common words to exclude
        stop_words = {'the', 'and', 'a', 'to', 'of', 'in', 'is', 'that', 'it', 'on', 'you', 'for', 'with', 'as', 'at'}
        
        # Count word frequencies
        words = []
        for comment in comments:
            text = comment['text'].lower()
            words.extend([word for word in text.split() if word not in stop_words])
        
        word_freq = Counter(words)
        common_topics = word_freq.most_common(10)
        
        return {
            'top_topics': [{'word': word, 'count': count} for word, count in common_topics],
            'total_unique_words': len(set(words))
        }
    
    def _analyze_comment_timeline(self, comments):
        """Analyze comment activity over time"""
        if not comments:
            return "No comments found"
        
        # Sort comments by publish date
        sorted_comments = sorted(comments, key=lambda x: x['published_at'])
        
        # Group comments by hour
        hourly_comments = {}
        for comment in sorted_comments:
            hour = datetime.fromisoformat(comment['published_at'].replace('Z', '+00:00')).hour
            hourly_comments[hour] = hourly_comments.get(hour, 0) + 1
        
        return {
            'total_comments': len(comments),
            'first_comment': sorted_comments[0]['published_at'],
            'last_comment': sorted_comments[-1]['published_at'],
            'hourly_distribution': hourly_comments,
            'peak_hour': max(hourly_comments.items(), key=lambda x: x[1])[0] if hourly_comments else None
        }

if __name__ == "__main__":
    analyzer = CommentAnalyzer(
        video_id="dQw4w9WgXcQ"  # Example video ID
    )
    print(analyzer.run()) 