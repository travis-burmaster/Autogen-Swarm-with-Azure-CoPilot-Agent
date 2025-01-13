
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from src.agents.copilot_agent import CopilotAgent

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create Copilot agent instance
copilot_agent = CopilotAgent(
    direct_line_secret=config["copilot"]["direct_line_secret"],
    name="CopilotAssistant"
)

# Function to initiate chat and capture response
async def initiate_and_get_response():
    try:
        # Use the generate_response method instead of _oai_messages
        response = await copilot_agent.generate_response(
            "Can you tell me the PTO policy at Northramp?"
        )
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# Start the conversation
if __name__ == "__main__":
    # Use asyncio to run the asynchronous function
    #loop = asyncio.get_event_loop()
    result = asyncio.run(initiate_and_get_response())
    print("Response from Copilot Agent:", result)


    # Create other agents
# user_proxy = UserProxyAgent(
#     name="User",
#     system_message="A human user"
# )
# # Create group chat
# groupchat = GroupChat(
#     agents=[copilot_agent],
#     messages=[],
#     max_round=12
# )

# # Create manager

# manager = GroupChatManager(
#     groupchat=groupchat,
#     system_message="You are a helpful coordinator"
# )

# code_agent = AssistantAgent(
#     name="Coder",
#     system_message="Expert programmer who writes code"
# )