from typing import Union, List
from agency_swarm import Agency
from agency_swarm.agents import Agent
from agency_swarm.util import set_openai_key
from trend_analyzer.tools.TrendAnalyzer import TrendAnalyzer
from trend_analyzer.tools.KeywordExtractor import KeywordExtractor
from trend_analyzer.tools.TavilySearchTool import TavilySearchTool
from trend_analyzer.tools.CompetitorAnalyzer import CompetitorAnalyzer
from trend_analyzer.tools.TrendVisualizer import TrendVisualizer
from dotenv import load_dotenv
import os
import json
import shutil

def test_trend_analyzer():
    print("\nTesting TrendAnalyzer...")
    try:
        analyzer = TrendAnalyzer(
            keywords=["artificial intelligence", "machine learning", "chatgpt"],
            timeframe="today 3-m"
        )
        result = analyzer.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ TrendAnalyzer test successful!")
            print("Sample of the result:")
            print(f"Analyzed keywords: {result_data.get('analyzed_keywords', [])}")
            print(f"Number of trends analyzed: {len(result_data.get('interest_over_time', {}))}")
            print(f"Timestamp: {result_data.get('timestamp', '')}")
            return result_data  # Return data for visualization test
    except Exception as e:
        print(f"❌ Error testing TrendAnalyzer: {str(e)}")
    return None

def test_keyword_extractor():
    print("\nTesting KeywordExtractor...")
    try:
        test_text = """
        Artificial intelligence and machine learning are revolutionizing industries in 2024.
        Large language models like GPT-4 are transforming how we interact with technology.
        Companies are increasingly adopting AI solutions for automation and data analysis.
        The rise of multimodal AI models is creating new opportunities for innovation.
        """
        extractor = KeywordExtractor(text=test_text, max_keywords=5)
        result = extractor.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ KeywordExtractor test successful!")
            print("Extracted keywords:")
            print(json.dumps(result_data['keywords'], indent=2))
            print(f"Total keywords found: {result_data['total_keywords_found']}")
    except Exception as e:
        print(f"❌ Error testing KeywordExtractor: {str(e)}")

def test_competitor_analyzer():
    print("\nTesting CompetitorAnalyzer...")
    try:
        analyzer = CompetitorAnalyzer(
            competitors=["OpenAI", "Anthropic", "Google AI"],
            industry_keywords=["artificial intelligence", "large language models", "AI safety"],
            analysis_timeframe="last_month"
        )
        result = analyzer.run()
        result_data = json.loads(result)
        
        if "error" in result_data:
            print(f"❌ {result_data['error']}")
        else:
            print("✅ CompetitorAnalyzer test successful!")
            print("Sample of the results:")
            for competitor, insights in result_data.get("competitor_insights", {}).items():
                print(f"\nCompetitor: {competitor}")
                print(f"Recent activities found: {len(insights.get('recent_activities', []))}")
                print("Keyword presence:", json.dumps(insights.get('keyword_presence', {}), indent=2))
    except Exception as e:
        print(f"❌ Error testing CompetitorAnalyzer: {str(e)}")

def test_trend_visualizer():
    print("\nTesting TrendVisualizer...")
    try:
        # Get trend data from TrendAnalyzer test
        trend_data = test_trend_analyzer()
        if not trend_data:
            print("❌ Skipping TrendVisualizer test due to missing trend data")
            return

        # Create visualizations directory
        vis_dir = 'visualizations'
        if os.path.exists(vis_dir):
            shutil.rmtree(vis_dir)
        os.makedirs(vis_dir)

        # Test different visualization types
        for vis_type in ['line', 'bar', 'heatmap']:
            visualizer = TrendVisualizer(
                trend_data=trend_data,
                visualization_type=vis_type,
                output_dir=vis_dir
            )
            result = visualizer.run()
            result_data = json.loads(result)
            
            if "error" in result_data:
                print(f"❌ Error in {vis_type} visualization: {result_data['error']}")
            else:
                print(f"✅ {vis_type.capitalize()} visualization test successful!")
                print(f"Generated files: {result_data.get('generated_files', [])}")
    except Exception as e:
        print(f"❌ Error testing TrendVisualizer: {str(e)}")

def test_tavily_search():
    print("\nTesting TavilySearchTool...")
    try:
        searcher = TavilySearchTool(
            query="Latest trends in AI and machine learning 2024",
            search_depth="basic"  # Using basic for faster testing
        )
        result = searcher.run()
        if isinstance(result, str) and result.startswith("Error"):
            print(f"❌ {result}")
        else:
            print("✅ TavilySearchTool test successful!")
            print("Sample of search results:")
            if isinstance(result, dict):
                if 'answer' in result:
                    print(f"Answer: {result['answer'][:200]}...")
                if 'results' in result:
                    print(f"Number of results: {len(result['results'])}")
    except Exception as e:
        print(f"❌ Error testing TavilySearchTool: {str(e)}")

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
        
        # Create an agent with all trend analysis tools
        agent = Agent(
            name="TrendAnalyzer",
            description="An agent that analyzes content trends, extracts keywords, and researches current trends.",
            instructions="""You are a trend analysis expert with multiple capabilities:
            1. You can analyze keyword trends using Google Trends data
            2. You can extract important keywords from text content
            3. You can search and analyze current trends using Tavily
            4. You can analyze competitor activities and trends
            5. You can create visualizations of trend data
            
            When analyzing trends:
            - Focus on identifying emerging patterns and shifts in interest
            - Consider seasonal factors and long-term trends
            - Look for related topics and queries that might be relevant
            - Analyze competitor activities and their impact
            - Create visual representations of trends when useful
            - Provide actionable insights based on the data""",
            tools=[TrendAnalyzer, KeywordExtractor, TavilySearchTool, CompetitorAnalyzer, TrendVisualizer],
            temperature=0.7,
            model="gpt-4-turbo-preview"  # Specify the model explicitly
        )
        print("✅ Agent created successfully!")
        
        # Create an agency with our trend analyzer
        agency = Agency(
            [agent],
            shared_instructions="You are part of a content creation agency focused on identifying and analyzing content trends.",
        )
        print("✅ Agency created successfully!")
        
        # Test the agent with a comprehensive task
        test_prompt = """Please analyze the current trends in AI by:
        1. Extracting key themes from this text: 'AI and machine learning are transforming industries in 2024, with a focus on automation and innovation.'
        2. Analyzing trends for key AI companies
        3. Creating visualizations of the trend data
        4. Searching for the latest AI developments in 2024
        
        Provide a comprehensive analysis of your findings."""
        
        print("\nTesting agent with comprehensive task...")
        print("\nAgent's response:")
        response = agency.get_completion(test_prompt)
        print(response)
        
    except Exception as e:
        print(f"❌ Error in agent integration: {str(e)}")

if __name__ == "__main__":
    print("=== Testing Individual Tools ===")
    test_keyword_extractor()  # Test KeywordExtractor first as it's most reliable
    test_tavily_search()      # Test Tavily search next
    test_trend_analyzer()     # Test TrendAnalyzer
    test_competitor_analyzer() # Test CompetitorAnalyzer
    test_trend_visualizer()   # Test TrendVisualizer last as it depends on TrendAnalyzer data
    
    print("\n=== Testing Agent Integration ===")
    test_agent_integration() 