from autogen import AssistantAgent
import requests
import time
import json
from typing import Dict, Optional

class CopilotAgent(AssistantAgent):
    def __init__(self, direct_line_secret: str, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://directline.botframework.com/v3/directline"
        self.secret = direct_line_secret
        self.conversation_id = None
        self.token = None
        self.watermark = None
        
    async def _init_conversation(self):
        """Initialize a new conversation with Direct Line"""
        try:
            # Generate token
            headers = {
                "Authorization": f"Bearer {self.secret}"
            }
            response = requests.post(
                f"{self.base_url}/tokens/generate",
                headers=headers
            )
            response.raise_for_status()
            token_data = response.json()
            print(f"Token response: {json.dumps(token_data, indent=2)}")
            self.token = token_data["token"]
            
            # Start conversation
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            response = requests.post(
                f"{self.base_url}/conversations",
                headers=headers
            )
            response.raise_for_status()
            conv_data = response.json()
            print(f"Conversation start response: {json.dumps(conv_data, indent=2)}")
            self.conversation_id = conv_data["conversationId"]
            
        except requests.exceptions.RequestException as e:
            print(f"Error in _init_conversation: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
            raise
        
    async def generate_response(self, message: str) -> str:
        try:
            if not self.conversation_id:
                await self._init_conversation()
                
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Send message
            activity = {
                "type": "message",
                "text": message,
                "from": {
                    "id": "user",
                    "name": "User"
                },
                "locale": "en-US",
                "textFormat": "plain"
            }
            
            print(f"Sending message: {json.dumps(activity, indent=2)}")
            
            response = requests.post(
                f"{self.base_url}/conversations/{self.conversation_id}/activities",
                headers=headers,
                json=activity
            )
            response.raise_for_status()
            send_data = response.json()
            print(f"Send message response: {json.dumps(send_data, indent=2)}")
            
            # Wait a moment for the bot to process
            time.sleep(2)
            
            # Get response with watermark if available
            url = f"{self.base_url}/conversations/{self.conversation_id}/activities"
            if self.watermark:
                url += f"?watermark={self.watermark}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            activities_data = response.json()
            print(f"Get activities response: {json.dumps(activities_data, indent=2)}")
            
            # Update watermark
            if 'watermark' in activities_data:
                self.watermark = activities_data['watermark']
            
            # Filter bot responses
            bot_responses = [
                activity["text"] 
                for activity in activities_data.get("activities", [])
                if activity.get("from", {}).get("role") == "bot"
            ]
            
            return bot_responses[-1] if bot_responses else "No response received"
            
        except requests.exceptions.RequestException as e:
            print(f"Error in generate_response: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
            return f"Error communicating with Copilot: {str(e)}"