import os
from dotenv import load_dotenv
import logging
from youtube_analyzer import YouTubeAnalyzer
from tools.VideoSearcher import VideoSearcher
from tools.VideoPerformanceAnalyzer import VideoPerformanceAnalyzer
from tools.CommentAnalyzer import CommentAnalyzer
from tools.ChannelAnalyzer import ChannelAnalyzer
from tools.CompetitorAnalyzer import CompetitorAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_video_searcher():
    """Test the VideoSearcher tool"""
    logger.info("\n=== Testing VideoSearcher ===")
    try:
        searcher = VideoSearcher(
            query="neural networks basics",
            max_results=5
        )
        results = searcher.run()
        logger.info(f"VideoSearcher Results: {results[:200]}...")
        return results
    except Exception as e:
        logger.error(f"Error in VideoSearcher: {str(e)}")
        raise

def test_video_performance_analyzer(video_id):
    """Test the VideoPerformanceAnalyzer tool"""
    logger.info("\n=== Testing VideoPerformanceAnalyzer ===")
    try:
        analyzer = VideoPerformanceAnalyzer(
            video_id=video_id
        )
        results = analyzer.run()
        logger.info(f"Performance Analysis Results: {results[:200]}...")
        return results
    except Exception as e:
        logger.error(f"Error in VideoPerformanceAnalyzer: {str(e)}")
        raise

def test_comment_analyzer(video_id):
    """Test the CommentAnalyzer tool"""
    logger.info("\n=== Testing CommentAnalyzer ===")
    try:
        analyzer = CommentAnalyzer(
            video_id=video_id,
            max_comments=10
        )
        results = analyzer.run()
        logger.info(f"Comment Analysis Results: {results[:200]}...")
        return results
    except Exception as e:
        logger.error(f"Error in CommentAnalyzer: {str(e)}")
        raise

def test_channel_analyzer(channel_id):
    """Test the ChannelAnalyzer tool"""
    logger.info("\n=== Testing ChannelAnalyzer ===")
    try:
        analyzer = ChannelAnalyzer(
            channel_id=channel_id
        )
        results = analyzer.run()
        logger.info(f"Channel Analysis Results: {results[:200]}...")
        return results
    except Exception as e:
        logger.error(f"Error in ChannelAnalyzer: {str(e)}")
        raise

def test_competitor_analyzer(channel_id):
    """Test the CompetitorAnalyzer tool"""
    logger.info("\n=== Testing CompetitorAnalyzer ===")
    try:
        analyzer = CompetitorAnalyzer(
            channel_id=channel_id
        )
        results = analyzer.run()
        logger.info(f"Competitor Analysis Results: {results[:200]}...")
        return results
    except Exception as e:
        logger.error(f"Error in CompetitorAnalyzer: {str(e)}")
        raise

def test_youtube_analyzer_agent():
    """Test the YouTube Analyzer agent as a whole"""
    logger.info("\n=== Testing YouTube Analyzer Agent ===")
    try:
        agent = YouTubeAnalyzer()
        logger.info("YouTube Analyzer agent initialized successfully")
        
        # Test with a sample query
        query = "neural networks basics"
        logger.info(f"Testing agent with query: {query}")
        
        response = agent._process_message(query)
        logger.info(f"Agent Response: {response[:200]}...")
        
        return response
    except Exception as e:
        logger.error(f"Error in YouTube Analyzer agent: {str(e)}")
        raise

def main():
    """Main test function"""
    logger.info("Starting YouTube Analyzer tests...")
    
    try:
        # Test individual tools
        video_search_results = test_video_searcher()
        
        # Extract video ID from search results for further testing
        # Note: This assumes VideoSearcher returns a JSON string with video IDs
        import json
        search_data = json.loads(video_search_results)
        if search_data and 'videos' in search_data and len(search_data['videos']) > 0:
            first_video = search_data['videos'][0]
            video_id = first_video.get('video_id')
            channel_id = first_video.get('channel_id')
            
            if video_id:
                test_video_performance_analyzer(video_id)
                test_comment_analyzer(video_id)
            
            if channel_id:
                test_channel_analyzer(channel_id)
                test_competitor_analyzer(channel_id)
        
        # Test the complete agent
        test_youtube_analyzer_agent()
        
        logger.info("All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main test: {str(e)}")
        raise

if __name__ == "__main__":
    main() 