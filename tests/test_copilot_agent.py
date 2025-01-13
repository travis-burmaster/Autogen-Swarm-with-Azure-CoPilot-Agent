import pytest
from unittest.mock import Mock, patch
from src.agents.copilot_agent import CopilotAgent

@pytest.fixture
def mock_copilot_agent():
    return CopilotAgent(
        endpoint_url="http://test.endpoint",
        auth_token="test_token",
        name="TestAgent"
    )

def test_agent_initialization(mock_copilot_agent):
    assert mock_copilot_agent.endpoint_url == "http://test.endpoint"
    assert mock_copilot_agent.auth_headers == {"Authorization": "Bearer test_token"}
    assert mock_copilot_agent.metrics["total_calls"] == 0

@patch("requests.post")
async def test_generate_response(mock_post, mock_copilot_agent):
    mock_response = Mock()
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    response = await mock_copilot_agent.generate_response("Test message")
    
    assert response == "Test response"
    assert mock_copilot_agent.metrics["total_calls"] == 1

def test_get_metrics(mock_copilot_agent):
    mock_copilot_agent.metrics = {
        "total_calls": 10,
        "total_latency": 5.0
    }
    
    metrics = mock_copilot_agent.get_metrics()
    
    assert metrics["average_latency"] == 0.5