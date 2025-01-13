# Autogen Swarm with Azure Copilot Agent Integration

This repository demonstrates how to integrate Azure Copilot Studio agents with Microsoft's Autogen framework for creating sophisticated multi-agent systems.

## Overview

This project showcases the integration between Azure Copilot Studio's custom agents and Autogen's swarm architecture, enabling:
- Seamless communication between Copilot agents and Autogen agents
- Enhanced multi-agent collaboration
- Scalable agent interactions
- Custom workflow orchestration

## Prerequisites

- Python 3.8+
- Azure Copilot Studio account with agent creation access
- Autogen library
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/travis-burmaster/Autogen-Swarm-with-Azure-CoPilot-Agent.git
cd Autogen-Swarm-with-Azure-CoPilot-Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your Azure Copilot Studio credentials in `config.yaml`

## Project Structure

```
├── src/
│   ├── agents/
│   │   ├── copilot_agent.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── api_wrapper.py
│   │   └── __init__.py
│   └── main.py
├── config/
│   └── config.yaml
├── examples/
│   └── basic_swarm.py
├── tests/
│   └── test_copilot_agent.py
├── requirements.txt
└── README.md
```

## Usage

1. Set up your Azure Copilot Studio agent and obtain the API endpoint and authentication token.

2. Configure your credentials in `config.yaml`:
```yaml
copilot:
  endpoint_url: "your_endpoint_url"
  auth_token: "your_auth_token"
```

3. Run the example:
```bash
python examples/basic_swarm.py
```

## Configuration

The `CopilotAgent` class can be configured with various parameters:

```python
copilot_agent = CopilotAgent(
    endpoint_url="your_endpoint_url",
    auth_token="your_auth_token",
    name="CopilotAssistant",
    max_consecutive_auto_reply=10,
    custom_parameters={
        "temperature": 0.7,
        "max_tokens": 1000
    }
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Contact

- Create an issue in this repository
- Reach out to the maintainers