# waii-mcp-hands-on-lab
Talk to your database using WAII and MCP through Claude Desktop

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
   - For Windows:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. **Project Setup**:
   ```bash
   # Clone this repository
   git clone git@github.com:waii-ai/waii-mcp-hands-on-lab.git

   # Initialize the project and set up the environment
   uv init waii-mcp-hands-on-lab
   cd waii-mcp-hands-on-lab
   ```

4. **Virtual Environment and Dependencies**:

   For macOS:
   ```bash
   # Create virtual environment and activate it
   uv venv
   source .venv/bin/activate

   # Install required packages
   uv add "mcp[cli]" httpx
   uv pip install waii-sdk-py pandas
   ```

   For Windows:
   ```powershell
   # Create virtual environment and activate it
   uv venv
   .venv\Scripts\activate

   # Install required packages
   uv add mcp[cli] httpx
   uv pip install waii-sdk-py pandas
   ```

5. **Configure Claude Desktop for MCP**:

   For detailed information about the configuration file and troubleshooting, see [MCP Server Configuration](lab-docs/config_file.md).

   For macOS:
   ```bash
   # Create the config directory if it doesn't exist
   mkdir -p ~/Library/Application\ Support/Claude
   
   # Copy the weather config file
   cp configs/weather_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Open and edit the config file with your preferred text editor
   # For example, using VS Code:
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   # Or using nano:
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   For Windows:
   ```powershell
   # Create the config directory if it doesn't exist
   New-Item -ItemType Directory -Force -Path "$env:AppData\Claude"
   
   # Copy the weather config file
   Copy-Item mcp_server/weather_config.json "$env:AppData\Claude\claude_desktop_config.json"
   
   # Open and edit the config file with your preferred text editor
   # For example, using VS Code:
   code $env:AppData\Claude\claude_desktop_config.json
   # Or using Notepad:
   notepad $env:AppData\Claude\claude_desktop_config.json
   ```

   In the config file, update the `--directory` path to point to your project's absolute path:
   ```json
   {
       "mcpServers": {
           "waii": {
               "command": "uv",
               "args": [
                   "--directory",
                   "/ABSOLUTE/PATH/TO/waii-mcp-hands-on-lab",
                   "run",
                   "servers/weather.py"
               ]
           }
       }
   }
   ```

   > **Note**: If you encounter a `uv` connection error (error message ENOENT), you may need to use the full path to the `uv` executable in the `command` field. You can get this by running:
   > - On MacOS/Linux: `which uv`
   > - On Windows: `where uv`
   > 
   > Copy the output path and replace `"command": "uv"` with the full path (e.g., `"command": "/usr/local/bin/uv"`).
   > This can happen when installing uv on MAcOS/Linux with `curl -LsSf https://astral.sh/uv/install.sh | sh`
   > 
   > For more detailed information about the configuration file, see [MCP Server Configuration](lab-docs/config_file.md).

6. **Test the MCP Server**:
   - Open Claude Desktop
     - You can see enabled mcp tools in the 'search and tools' drop down (located on the bottom left, next to the '+')
   - Ask a question like "What's the weather in San Francisco?"
   - You should see Claude use the MCP server to fetch weather information
     - Claude should ask if it can trust the tool
   - If you see weather data in the response, your MCP server is working correctly!

## References

- [Model Context Protocol Server Documentation](https://modelcontextprotocol.io/quickstart/server) - Official guide for building MCP servers
- [Claude Desktop Download](https://claude.ai/download) - Download Claude Desktop application
