from agency_swarm import Agent
import json
import traceback

class ContentManager(Agent):
    def __init__(self):
        print("\n=== Content Manager Agent Initialization ===")
        super().__init__(
            name="Content Manager",
            description="Manages content strategy and coordinates between different analysis tools.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.7,
            max_prompt_tokens=25000
        )
        print("Content Manager Agent initialized successfully")
        print("=== End Content Manager Initialization ===\n")

    def _process_message(self, message):
        """
        Override the message processing to add logging
        """
        print("\n=== Content Manager Processing Message ===")
        print(f"Received message: {message[:200]}...")  # Print first 200 chars of message
        
        try:
            # Log available tools and agents
            print("\nAvailable Tools:")
            for tool in self.tools:
                print(f"- {tool.__class__.__name__}")
            
            print("\nAvailable Agents:")
            for agent in self.available_agents:
                print(f"- {agent.name}")
            
            # Process the message using parent class method
            print("\nProcessing message with parent class...")
            response = super()._process_message(message)
            
            print("\nContent Manager Response:")
            print(f"Response type: {type(response)}")
            print(f"Response preview: {str(response)[:200]}...")
            
            # Log any tool usage
            if hasattr(self, '_last_tool_used'):
                print(f"Last tool used: {self._last_tool_used}")
            
            # Log any agent communication
            if hasattr(self, '_last_agent_communication'):
                print(f"Last agent communication: {self._last_agent_communication}")
            
            # Log message processing steps
            print("\nMessage Processing Steps:")
            if hasattr(self, '_processing_steps'):
                for step in self._processing_steps:
                    print(f"- {step}")
            
            print("=== End Content Manager Processing ===\n")
            return response
            
        except Exception as e:
            error_msg = f"Error in Content Manager: {str(e)}\n{traceback.format_exc()}"
            print(f"ERROR: {error_msg}")
            return f"Error occurred during content management: {str(e)}"

    def _should_use_youtube_analyzer(self, message):
        """
        Helper method to determine if YouTube analysis is needed
        """
        print("\nEvaluating need for YouTube analysis...")
        # Log the decision-making process
        print(f"Message content: {message[:200]}...")
        
        # Add your logic here for when to use YouTube Analyzer
        # For now, we'll log that we're checking
        print("Checking message content for YouTube analysis triggers...")
        
        # Example triggers (you can modify these based on your needs)
        triggers = [
            "youtube", "video", "channel", "content", "analysis",
            "performance", "engagement", "views", "likes", "comments"
        ]
        
        message_lower = message.lower()
        found_triggers = [trigger for trigger in triggers if trigger in message_lower]
        
        print(f"Found triggers: {found_triggers}")
        should_use = len(found_triggers) > 0
        
        print(f"Decision: {'Will use' if should_use else 'Will not use'} YouTube Analyzer")
        return should_use