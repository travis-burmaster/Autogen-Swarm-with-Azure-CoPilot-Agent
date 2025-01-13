import yaml
import asyncio
from autogen import UserProxyAgent, GroupChat, GroupChatManager, AssistantAgent
from src.agents.copilot_agent import CopilotAgent

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create Copilot agent instance
copilot_agent = CopilotAgent(
    direct_line_secret=config["copilot"]["direct_line_secret"],
    user_token=config["copilot"].get("user_token"),  # Optional user token
    name="CopilotAssistant"
)

# Create other agents
user_proxy = UserProxyAgent(
    name="User",
    system_message="A human user"
)

code_agent = AssistantAgent(
    name="Coder",
    system_message="Expert programmer who writes code"
)

# Create group chat
groupchat = GroupChat(
    agents=[user_proxy, copilot_agent, code_agent],
    messages=[],
    max_round=12
)

# Create manager
manager = GroupChatManager(
    groupchat=groupchat,
    system_message="You are a helpful coordinator"
)

# Test the Copilot agent directly first
async def test_copilot():
    try:
        test_messages = [
            "Hello, how are you?",
            "Can you tell me about the company policies?"
        ]
        
        for message in test_messages:
            print(f"\nSending message: {message}")
            response = await copilot_agent.generate_response(message)
            print(f"Response from Copilot Agent: {response}\n")
            
            if "Authentication required" in response:
                print("Please complete the authentication process using the provided URL")
                auth_token = input("After authentication, please enter the token (or press Enter to skip): ").strip()
                if auth_token:
                    copilot_agent.user_token = auth_token
                    print("\nRetrying with authentication token...")
                    response = await copilot_agent.generate_response(message)
                    print(f"New response: {response}")
            
            await asyncio.sleep(2)  # Wait between messages
            
    except Exception as e:
        print(f"Error: {str(e)}")

# Start the conversation
if __name__ == "__main__":
    asyncio.run(test_copilot())
    # Uncomment below to run the full group chat
    # user_proxy.initiate_chat(
    #     manager,
    #     message="Let's solve this problem..."
    # )