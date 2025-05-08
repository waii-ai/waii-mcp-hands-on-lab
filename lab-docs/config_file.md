# MCP Server Configuration

The MCP server configuration file (`claude_desktop_config.json`) is a crucial component that tells Claude how to start and connect to your MCP server. We have placed template files in the `configs` directory of your project.

## Step 1: Update the Configuration File

First, you'll need to update the `config.json` configuration file in your project's `configs` directory. Here's the structure you'll need to modify:

```json
{
    "mcpServers": {
        "waii": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/waii-mcp-hands-on-lab",
                "run",
                "servers/waii_mcp_server.py",
                "--api-key",
                "<fill in your api key>"
            ]
        }
    }
}
```

Make sure to:
1. Replace `/ABSOLUTE/PATH/TO/waii-mcp-hands-on-lab` with the actual absolute path to your project
2. Replace `<fill in your api key>` with the WAII API key provided to you

## Step 2: Copy to Claude's Config Directory

After updating the configuration file, you'll need to copy it to Claude's configuration directory:

### For Mac Users
```bash
# Create the config directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude

# Copy the config file
cp configs/config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### For Windows Users
```powershell
# Create the config directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:AppData\Claude"

# Copy the config file
Copy-Item "configs\config.json" "$env:AppData\Claude\claude_desktop_config.json"
```

## Configuration Components

Let's break down each part of the configuration:

1. **mcpServers**: The top-level object that contains all MCP server configurations
   - Each server is identified by a unique key (in this case, "waii")

2. **Server Configuration**:
   - `command`: The command to use to start the server (in this case, "uv")
   - `args`: An array of arguments to pass to the command:
     - `--directory`: The absolute path to your project directory
     - `run`: The subcommand to run the Python file
     - `servers/waii_mcp_server.py`: The path to your server implementation
     - `--api-key`: The flag for the WAII API key
     - `<fill in your api key>`: Your actual WAII API key

## How It Works

This configuration file serves several important purposes:

1. **Server Location**: Tells Claude where to find your server implementation
2. **Startup Command**: Specifies how to start the server (using `uv` in this case)
3. **Environment Setup**: Provides the necessary directory context for the server
4. **Authentication**: Includes the WAII API key for database access

## Usage

When Claude needs to use your MCP server:
1. It reads this configuration file
2. Uses the specified command and arguments to start the server
3. Connects to the server to make tool calls

## Important Notes

1. **Path Configuration**: 
   - Replace `/ABSOLUTE/PATH/TO/waii-mcp-hands-on-lab` with the actual absolute path to your project
   - Make sure the path is correct for your system

2. **API Key**:
   - Replace `<fill in your api key>` with your actual WAII API key
   - Keep this file secure and don't commit it to version control

3. **Server Name**:
   - The server name ("waii" in this case) should match the name used in your FastMCP initialization
   - This name is used to identify the server in tool declarations

## Example Usage in Code

This configuration is used when you initialize your MCP server:

```python
from mcp.server import FastMCP

# The name "waii" should match the key in your config.json
mcp = FastMCP("waii")
```

## Testing the Configuration

To test if your configuration is correct:
1. Make sure the paths are correct for your system
2. Verify that your API key is valid
3. Try running the server manually using the command specified in the configuration
4. Check that Claude can successfully start and connect to your server
