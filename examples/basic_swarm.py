import yaml
from autogen import UserProxyAgent, GroupChat, GroupChatManager, AssistantAgent
from src.agents.copilot_agent import CopilotAgent

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create Copilot agent instance
copilot_agent = CopilotAgent(
    direct_line_secret=config["copilot"]["direct_line_secret"],
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
        response = await copilot_agent.generate_response("Hello, how are you?")
        print(f"Response from Copilot Agent: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Start the conversation
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_copilot())
    # Uncomment below to run the full group chat
    # user_proxy.initiate_chat(
    #     manager,
    #     message="Let's solve this problem..."
    # )