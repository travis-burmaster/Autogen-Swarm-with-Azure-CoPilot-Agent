from autogen import AssistantAgent
import requests
import time
from typing import Dict, Optional

class CopilotAgent(AssistantAgent):
    def __init__(self, direct_line_secret: str, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://directline.botframework.com/v3/directline"
        self.secret = direct_line_secret
        self.conversation_id = None
        self.token = None
        
    async def _init_conversation(self):
        """Initialize a new conversation with Direct Line"""
        headers = {
            "Authorization": f"Bearer {self.secret}"
        }
        response = requests.post(
            f"{self.base_url}/tokens/generate",
            headers=headers
        )
        response.raise_for_status()
        self.token = response.json()["token"]
        
        # Start conversation
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(
            f"{self.base_url}/conversations",
            headers=headers
        )
        response.raise_for_status()
        self.conversation_id = response.json()["conversationId"]
        
    async def generate_response(self, message: str) -> str:
        if not self.conversation_id:
            await self._init_conversation()
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Send message
        response = requests.post(
            f"{self.base_url}/conversations/{self.conversation_id}/activities",
            headers=headers,
            json={
                "type": "message",
                "text": message
            }
        )
        response.raise_for_status()
        
        # Get response
        response = requests.get(
            f"{self.base_url}/conversations/{self.conversation_id}/activities",
            headers=headers
        )
        response.raise_for_status()
        
        activities = response.json()["activities"]
        bot_responses = [
            activity["text"] 
            for activity in activities 
            if activity["from"]["role"] == "bot"
        ]
        
        return bot_responses[-1] if bot_responses else "No response received"
    def __init__(self, direct_line_secret: str, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://directline.botframework.com/v3/directline"
        self.secret = direct_line_secret
        self.conversation_id = None
        self.token = None
        
    async def _init_conversation(self):
        """Initialize a new conversation with Direct Line"""
        headers = {
            "Authorization": f"Bearer {self.secret}"
        }
        response = requests.post(
            f"{self.base_url}/tokens/generate",
            headers=headers
        )
        response.raise_for_status()
        self.token = response.json()["token"]
        
        # Start conversation
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(
            f"{self.base_url}/conversations",
            headers=headers
        )
        response.raise_for_status()
        self.conversation_id = response.json()["conversationId"]
        
    async def generate_response(self, message: str) -> str:
        if not self.conversation_id:
            await self._init_conversation()
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Send message
        response = requests.post(
            f"{self.base_url}/conversations/{self.conversation_id}/activities",
            headers=headers,
            json={
                "type": "message",
                "text": message
            }
        )
        response.raise_for_status()
        
        # Get response
        response = requests.get(
            f"{self.base_url}/conversations/{self.conversation_id}/activities",
            headers=headers
        )
        response.raise_for_status()
        
        activities = response.json()["activities"]
        bot_responses = [
            activity["text"] 
            for activity in activities 
            if activity["from"]["role"] == "bot"
        ]
        
        return bot_responses[-1] if bot_responses else "No response received"

        # super().__init__(**kwargs)
        # self.endpoint_url = endpoint_url
        # self.auth_headers = {"Authorization": f"Bearer {auth_token}"}
        # self.metrics: Dict[str, float] = {
        #     "total_calls": 0,
        #     "total_latency": 0
        # }
    