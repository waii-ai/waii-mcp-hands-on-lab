# waii-mcp-hands-on-lab
Talk to your database using Waii and MCP through Claude Desktop

## System Requirements

- Python 3.10 or higher

# Prerequisites and Setup Instructions

Before proceeding with the lab, please follow the installation instructions in the [Prerequisites](#prerequisites) section below.

## Prerequisites

Make sure you have the following installed and configured:

1. **Claude Desktop** - Download and install Claude Desktop from [claude.ai/download](https://claude.ai/download)

2. **uv** - A fast Python package installer and resolver
   - For macOS:
     ```bash
     brew install uv
     ```
   - For Linux:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - For Windows:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. **Project Setup**:
   ```bash
   # Clone this repository
   git clone git@github.com:waii-ai/waii-mcp-hands-on-lab.git

   # Change into the project directory
   cd waii-mcp-hands-on-lab
   ```

4. **Virtual Environment and Dependencies**:

   For macOS:
   ```bash
   # Initialize the project and set up the environment
   uv init

   # Create virtual environment and activate it
   uv venv
   source .venv/bin/activate

   # Install required packages
   uv add "mcp[cli]" httpx
   uv pip install waii-sdk-py pandas
   ```

   For Windows:
   ```powershell
   # Initialize the project and set up the environment
   uv init

   # Create virtual environment and activate it
   uv venv
   .venv\Scripts\activate

   # Install required packages
   uv add mcp[cli] httpx
   uv pip install waii-sdk-py pandas
   ```

5. **Next steps**:

Please proceed to [MCP Server Configuration](lab-docs/1_configuring_waii_mcp_server.md) to setup the prebuilt Waii MCP server.
If you need more information, you can refer to:
  - [MCP basics](lab-docs/ref_understand_the_basics.md)
  - [Building the Waii MCP server step-by-step](lab-docs/ref_building_mcp_server.md)

## References

- [Model Context Protocol Server Documentation](https://modelcontextprotocol.io/quickstart/server) - Official guide for building MCP servers
- [Claude Desktop Download](https://claude.ai/download) - Download Claude Desktop application
