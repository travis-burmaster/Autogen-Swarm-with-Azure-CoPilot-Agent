from autogen import AssistantAgent
import requests
import time
from typing import Dict, Optional

class CopilotAgent2(AssistantAgent):
    def __init__(self, endpoint_url: str, auth_token: str, **kwargs):
        super().__init__(**kwargs)
        self.endpoint_url = endpoint_url
        self.auth_headers = {"Authorization": f"Bearer {auth_token}"}
        self.metrics: Dict[str, float] = {
            "total_calls": 0,
            "total_latency": 0
        }
    
    async def generate_response(self, message: str) -> str:
        """Generate a response using the Copilot Studio agent.

        Args:
            message: The input message to process

        Returns:
            str: The generated response from the Copilot agent
        """
        start_time = time.time()
        self.metrics["total_calls"] += 1
        
        try:
            response = requests.post(
                self.endpoint_url,
                headers=self.auth_headers,
                json={"message": message},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()["response"]
        except requests.exceptions.RequestException as e:
            result = f"Error communicating with Copilot: {str(e)}"
        
        latency = time.time() - start_time
        self.metrics["total_latency"] += latency
        
        return result
    
    def get_metrics(self) -> Dict[str, float]:
        """Get the current metrics for the agent.

        Returns:
            Dict[str, float]: Dictionary containing metrics
        """
        avg_latency = (
            self.metrics["total_latency"] / self.metrics["total_calls"]
            if self.metrics["total_calls"] > 0
            else 0
        )
        
        return {
            **self.metrics,
            "average_latency": avg_latency
        }