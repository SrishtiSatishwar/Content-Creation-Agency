from agency_swarm import Agency
from agency_swarm.agents import Agent
from agency_swarm.util import set_openai_key
from youtube_analyzer.tools.CommentAnalyzer import CommentAnalyzer
from youtube_analyzer.tools.CompetitorAnalyzer import CompetitorAnalyzer
from youtube_analyzer.tools.VideoPerformanceAnalyzer import VideoPerformanceAnalyzer
from youtube_analyzer.tools.ChannelAnalyzer import ChannelAnalyzer
from dotenv import load_dotenv
import os
import json

def test_channel_analyzer():
    print("\nTesting ChannelAnalyzer...")
    try:
        analyzer = ChannelAnalyzer(
            channel_id="UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast's channel ID
            metrics=["subscribers", "views", "videos"]
        )
        result = analyzer.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ ChannelAnalyzer test successful!")
            print("Sample of the result:")
            print(json.dumps(result_data, indent=2))
    except Exception as e:
        print(f"❌ Error testing ChannelAnalyzer: {str(e)}")

def test_video_performance_analyzer():
    print("\nTesting VideoPerformanceAnalyzer...")
    try:
        analyzer = VideoPerformanceAnalyzer(
            channel_id="UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast's channel ID
            time_range="30d"
        )
        result = analyzer.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ VideoPerformanceAnalyzer test successful!")
            print("Sample of the result:")
            print(json.dumps(result_data, indent=2))
    except Exception as e:
        print(f"❌ Error testing VideoPerformanceAnalyzer: {str(e)}")

def test_comment_analyzer():
    print("\nTesting CommentAnalyzer...")
    try:
        analyzer = CommentAnalyzer(
            video_id="-4GmbBoYQjE",  # MrBeast's recent video "I Explored 2000 Year Old Ancient Temples"
            max_comments=100,
            analyze_sentiment=True
        )
        result = analyzer.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ CommentAnalyzer test successful!")
            print("Sample of the result:")
            print("Total comments analyzed:", len(result_data.get("comments", [])))
            print("Sentiment summary:", result_data.get("sentiment_summary", {}))
    except Exception as e:
        print(f"❌ Error testing CommentAnalyzer: {str(e)}")

def test_youtube_competitor_analyzer():
    print("\nTesting YouTube CompetitorAnalyzer...")
    try:
        analyzer = CompetitorAnalyzer(
            competitor_ids=[
                "UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast
                "UC-lHJZR3Gqxm24_Vd_AJ5Yw"  # PewDiePie
            ],
            metrics=["subscribers", "views", "videos", "engagement"]
        )
        result = analyzer.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ YouTube CompetitorAnalyzer test successful!")
            print("Sample of the results:")
            print(json.dumps(result_data, indent=2))
    except Exception as e:
        print(f"❌ Error testing YouTube CompetitorAnalyzer: {str(e)}")

def test_agent_integration():
    print("\n=== Testing Agent Integration ===\n")
    try:
        # Load environment variables
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
        
        # Set OpenAI key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        set_openai_key(openai_key)
        
        # Create an agent with all YouTube analysis tools
        agent = Agent(
            name="YouTubeAnalyzer",
            description="An agent that analyzes YouTube channels, videos, comments, and competitors.",
            instructions="""You are a YouTube analysis expert with multiple capabilities:
            1. You can analyze YouTube channel metrics and performance
            2. You can analyze video performance and engagement
            3. You can analyze video comments and sentiment
            4. You can analyze competitor channels and their performance
            
            When analyzing YouTube content:
            - Focus on identifying trends and patterns in performance
            - Consider engagement metrics and audience response
            - Look for opportunities for improvement
            - Compare performance with competitors
            - Provide actionable insights based on the data""",
            tools=[ChannelAnalyzer, VideoPerformanceAnalyzer, CommentAnalyzer, CompetitorAnalyzer],
            temperature=0.7,
            model="gpt-4-turbo-preview"
        )
        print("✅ Agent created successfully!")
        
        # Create an agency with our YouTube analyzer
        agency = Agency(
            [agent],
            shared_instructions="You are part of a content creation agency focused on YouTube content analysis and optimization.",
        )
        print("✅ Agency created successfully!")
        
        # Test the agent with a comprehensive task
        test_prompt = """Please analyze this YouTube channel and video:
        1. Channel: MrBeast (UCX6OQ3DkcsbYNE6H8uQQuVA)
        2. Video: jG0Ys_5YK1k
        3. Compare with PewDiePie's channel
        
        Provide a comprehensive analysis including:
        - Channel performance metrics
        - Video performance and engagement
        - Comment sentiment analysis
        - Competitor comparison
        
        What insights can you provide for improvement?"""
        
        print("\nTesting agent with comprehensive task...")
        print("\nAgent's response:")
        response = agency.get_completion(test_prompt)
        print(response)
        
    except Exception as e:
        print(f"❌ Error in agent integration: {str(e)}")

if __name__ == "__main__":
    print("=== Testing Individual Tools ===")
    test_channel_analyzer()
    test_video_performance_analyzer()
    test_comment_analyzer()
    test_youtube_competitor_analyzer()
    
    print("\n=== Testing Agent Integration ===")
    test_agent_integration() 