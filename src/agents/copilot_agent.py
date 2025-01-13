from autogen import AssistantAgent
import requests
import time
import json
from typing import Dict, Optional

class CopilotAgent(AssistantAgent):
    def __init__(self, api_key: str, region: str, environment_id: str, **kwargs):
        super().__init__(**kwargs)
        self.base_url = f"https://{region}.microsoft.com/powervirtualagents/v1/environments/{environment_id}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session_id = None
        
    async def _init_session(self):
        """Initialize a new session"""
        try:
            response = requests.post(
                f"{self.base_url}/sessions",
                headers=self.headers,
                json={}
            )
            response.raise_for_status()
            session_data = response.json()
            print(f"Session response: {json.dumps(session_data, indent=2)}")
            self.session_id = session_data.get('session_id')
            
        except requests.exceptions.RequestException as e:
            print(f"Error in _init_session: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
            raise
        
    async def generate_response(self, message: str) -> str:
        try:
            if not self.session_id:
                await self._init_session()
                
            # Send message
            response = requests.post(
                f"{self.base_url}/sessions/{self.session_id}/messages",
                headers=self.headers,
                json={
                    "message": message
                }
            )
            response.raise_for_status()
            message_data = response.json()
            print(f"Message response: {json.dumps(message_data, indent=2)}")
            
            # Extract bot response
            messages = message_data.get('messages', [])
            bot_responses = [
                msg['text'] 
                for msg in messages 
                if msg.get('sender') == 'bot' and 'text' in msg
            ]
            
            return bot_responses[-1] if bot_responses else "No response received"
            
        except Exception as e:
            print(f"Error in generate_response: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
            return f"Error communicating with Copilot: {str(e)}"