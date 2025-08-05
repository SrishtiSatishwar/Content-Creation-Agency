from agency_swarm import Agency
from agency_swarm.agents import Agent
from agency_swarm.util import set_openai_key
from content_manager.tools.sentiment_analyzer import SentimentAnalyzer
from content_manager.tools.ScriptWriter import ScriptWriter
from content_manager.tools.OpenAIContentGenerator import OpenAIContentGenerator
from dotenv import load_dotenv
import os

def create_content_manager():
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    
    # Set OpenAI key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    set_openai_key(openai_key)
    
    # Create an agent with all content management tools
    agent = Agent(
        name="ContentManager",
        description="A comprehensive content management agent that can analyze sentiment, generate content, and write scripts.",
        instructions="""You are a versatile content manager with multiple capabilities:
        1. You can analyze the sentiment and emotional tone of text
        2. You can generate creative content ideas
        3. You can write and save scripts in markdown format
        
        Use your tools appropriately based on the task at hand.""",
        tools=[SentimentAnalyzer, ScriptWriter, OpenAIContentGenerator],
        temperature=0.7
    )
    
    return agent

def test_tools():
    print("\n=== Testing Individual Tools ===\n")
    
    # Test SentimentAnalyzer
    print("Testing SentimentAnalyzer...")
    test_text = "I'm really excited about this new AI technology! It's fascinating."
    analyzer = SentimentAnalyzer(text=test_text)
    print(f"Sentiment Analysis Result: {analyzer.run()}\n")
    
    # Test OpenAIContentGenerator
    print("Testing OpenAIContentGenerator...")
    generator = OpenAIContentGenerator(
        prompt="Generate a short video script idea about AI and creativity",
        temperature=0.7
    )
    print(f"Content Generation Result: {generator.run()}\n")
    
    # Test ScriptWriter
    print("Testing ScriptWriter...")
    writer = ScriptWriter(
        content="# Test Script\n\nThis is a test script generated during tool testing.",
        file_name="test_script"
    )
    print(f"Script Writing Result: {writer.run()}\n")

def test_agent_integration():
    print("\n=== Testing Agent Integration ===\n")
    
    try:
        print("Creating Content Manager agent...")
        agent = create_content_manager()
        print("✅ Agent created successfully!")
        
        # Create an agency with our content manager
        agency = Agency(
            [agent],
            shared_instructions="You are part of a content creation agency focused on creating and analyzing engaging content.",
        )
        print("✅ Agency created successfully!")
        
        # Test the agent with a complex task that uses multiple tools
        test_prompt = """Please help me with the following tasks:
        1. Generate a creative video script idea about AI in education
        2. Analyze the sentiment of this feedback: 'The video was incredibly informative and engaging!'
        3. Save the generated script as 'ai_education_script.md'"""
        
        print("\nTesting agent with complex task...")
        print("\nAgent's response:")
        response = agency.get_completion(test_prompt)
        print(response)
        
    except Exception as e:
        print("❌ Error:", str(e))

if __name__ == "__main__":
    try:
        # Test individual tools first
        test_tools()
        
        # Then test agent integration
        test_agent_integration()
        
    except Exception as e:
        print("❌ Error:", str(e)) 