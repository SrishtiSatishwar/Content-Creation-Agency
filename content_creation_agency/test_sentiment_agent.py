from agency_swarm import Agency
from agency_swarm.agents import Agent
from agency_swarm.util import set_openai_key
from content_manager.tools.sentiment_analyzer import SentimentAnalyzer
from dotenv import load_dotenv
import os

def create_sentiment_agent():
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    
    # Set OpenAI key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    set_openai_key(openai_key)
    
    # Create an agent with the sentiment analysis tool
    agent = Agent(
        name="ContentAnalyst",
        description="An agent that analyzes the sentiment of text content.",
        instructions="""You are a content analyst who specializes in understanding the emotional tone and sentiment of text.
        When given text content, analyze its sentiment and provide insights about its emotional tone.
        Use the sentiment analyzer tool to support your analysis with data.""",
        tools=[SentimentAnalyzer],
        temperature=0.7
    )
    
    return agent

if __name__ == "__main__":
    try:
        print("Creating Content Analyst agent...")
        agent = create_sentiment_agent()
        print("✅ Agent created successfully!")
        
        # Create an agency with just our sentiment agent
        agency = Agency(
            [agent],  # List of agents, with our agent as the entry point
            shared_instructions="You are part of a content creation agency focused on analyzing and creating engaging content.",
        )
        print("✅ Agency created successfully!")
        
        # Test the agent with some sample text
        test_text = "I'm really excited about this new AI technology! It's fascinating how it can help us be more productive, although there are some challenges to consider."
        
        print("\nTesting agent with sample text:")
        print(f"Text: {test_text}")
        print("\nAgent's analysis:")
        
        # Get the agent's analysis through the agency
        response = agency.get_completion(
            f"Please analyze the sentiment of this text and provide your insights: '{test_text}'"
        )
        
        print("\nAgent's response:")
        print(response)
        
    except Exception as e:
        print("❌ Error:", str(e)) 