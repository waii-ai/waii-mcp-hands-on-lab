# waii-mcp-hands-on-lab
Talk to your database using WAII and MCP through Claude Desktop

## Prerequisites 

Before you begin, we will use a basic MCP server to confirm the environment. 
Make sure you have the following installed and configured:

1. **Claude Desktop** - Download and install Claude Desktop from [claude.ai/download](https://claude.ai/download)

2. **uv** - A fast Python package installer and resolver
   - For macOS:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - For Windows:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. **Project Setup**:
   ```bash
   # Clone the repository
   git clone https://github.com/your-username/waii-mcp-hands-on-lab.git

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
   uv pip install waii-sdk-py
   ```

   For Windows:
   ```powershell
   # Create virtual environment and activate it
   uv venv
   .venv\Scripts\activate

   # Install required packages
   uv add mcp[cli] httpx
   uv pip install waii-sdk-py
   ```

5. **Configure Claude Desktop for MCP**:

   For macOS:
   ```bash
   # Create the config directory if it doesn't exist
   mkdir -p ~/Library/Application\ Support/Claude
   
   # Copy the weather config file
   cp configs/weather_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Edit the config file to update the directory path
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   For Windows:
   ```powershell
   # Create the config directory if it doesn't exist
   New-Item -ItemType Directory -Force -Path "$env:AppData\Claude"
   
   # Copy the weather config file
   Copy-Item mcp_server/weather_config.json "$env:AppData\Claude\claude_desktop_config.json"
   
   # Edit the config file to update the directory path
   code $env:AppData\Claude\claude_desktop_config.json
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

6. **Test the MCP Server**:
   - Open Claude Desktop
   - Ask a question like "What's the weather in San Francisco?"
   - You should see Claude use the MCP server to fetch weather information
   - If you see weather data in the response, your MCP server is working correctly!

## References

- [Model Context Protocol Server Documentation](https://modelcontextprotocol.io/quickstart/server) - Official guide for building MCP servers
- [Claude Desktop Download](https://claude.ai/download) - Download Claude Desktop application
