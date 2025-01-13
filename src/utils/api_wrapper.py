import requests
from typing import Dict, Optional

class CopilotAPIWrapper:
    def __init__(self, endpoint_url: str, auth_token: str):
        """Initialize the API wrapper.

        Args:
            endpoint_url: The Copilot Studio agent endpoint URL
            auth_token: Authentication token for the API
        """
        self.endpoint_url = endpoint_url
        self.auth_headers = {"Authorization": f"Bearer {auth_token}"}
    
    def make_request(
        self,
        message: str,
        custom_params: Optional[Dict] = None
    ) -> Dict:
        """Make a request to the Copilot Studio agent.

        Args:
            message: The message to send to the agent
            custom_params: Optional additional parameters

        Returns:
            Dict: The response from the agent
        """
        payload = {"message": message}
        if custom_params:
            payload.update(custom_params)
        
        response = requests.post(
            self.endpoint_url,
            headers=self.auth_headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        return response.json()