import yaml
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from src.agents.copilot_agent import CopilotAgent

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create Copilot agent instance
copilot_agent = CopilotAgent(
    endpoint_url=config["copilot"]["endpoint_url"],
    auth_token=config["copilot"]["auth_token"],
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

# Start the conversation
if __name__ == "__main__":
    user_proxy.initiate_chat(
        manager,
        message="Let's solve this problem..."
    )