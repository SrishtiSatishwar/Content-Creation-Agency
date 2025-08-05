from agency_swarm.agents import Agent
from agency_swarm.util import set_openai_key
from dotenv import load_dotenv
import os

def test_basic_setup():
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    
    # Set OpenAI key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please ensure your .env file is in the content_creation_agency directory.")
    
    print("✅ Successfully loaded environment variables")
    print("✅ Found OPENAI_API_KEY")
    
    set_openai_key(openai_key)
    print("✅ Set OpenAI key successfully")
    
    # Create a simple test agent
    test_agent = Agent(
        name="TestAgent",
        description="A simple test agent to verify our setup.",
        instructions="You are a test agent. Simply respond with 'Hello, I am working!' to verify the setup.",
        temperature=0.7
    )
    
    return test_agent

if __name__ == "__main__":
    try:
        print("Starting basic setup test...")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Looking for .env file in: {os.path.dirname(__file__)}")
        
        agent = test_basic_setup()
        print("✅ Basic setup successful!")
        print("Testing agent initialization...")
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print("❌ Setup failed with error:", str(e)) 