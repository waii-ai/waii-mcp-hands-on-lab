# MCP Server Configuration

We will now configure the Waii MCP server using the prebuilt implementation `servers/waii_mcp_server.py`.
If you want to do this yourself, please refer to [Building Waii MCP Server](lab-docs/ref_building_mcp_server.md)

Even though we have provided a completed server, the server still needs to be registered with Claude.  The MCP server configuration file (`claude_desktop_config.json`) is a crucial component that tells Claude how to start and connect to your MCP server. We have placed templated configuration files in the `configs` directory of your project.

## Step 1: Update the Configuration File

First, you'll need to update the `config.json` configuration file in your project's `configs` directory. Here's the structure you'll need to modify:

```json
{
    "mcpServers": {
        "waii": {
            "command": "/ABSOLUTE/PATH/TO/uv",  # TODO: fill in path (use `which uv` or `where uv`)
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/waii-mcp-hands-on-lab",  # TODO: fill in path
                "run",
                "servers/waii_mcp_server.py",
                "--api-key",
                "<fill in your api key>"  # TODO: fill in api key
            ]
        }
    }
}
```

Make sure to:
1. Replace `/ABSOLUTE/PATH/TO/waii-mcp-hands-on-lab` with the actual absolute path to your project
2. Replace `<fill in your api key>` with the Waii API key provided to you during the lab
3. Put the full path to the `uv` executable in the `command` field. You can get this by running:
   - On MacOS/Linux: `which uv`
   - On Windows: `where uv`

For example, if 
  - `which uv` returns `/usr/local/bin/uv`
  - `pwd` returns `/Users/waii_hands_on_lab/waii-mcp-hands-on-lab`
  - We provide the api key: `xxx123`
Your completed configuration file should be:
```json
{
    "mcpServers": {
        "waii": {
            "command": "/usr/local/bin/uv",
            "args": [
                "--directory",
                "/Users/waii_hands_on_lab/waii-mcp-hands-on-lab",
                "run",
                "servers/waii_mcp_server.py",
                "--api-key",
                "xxx123"
            ]
        }
    }
}
```

## Step 2: Copy and Edit the Configuration File for Claude Desktop

After updating the configuration file as described above, you'll need to copy it to Claude's configuration directory and edit it as needed:

### For Mac Users
```bash
# Create the config directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude

# Copy the config file
cp configs/config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Open and edit the config file with your preferred text editor
vim ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### For Windows Users
```powershell
# Create the config directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:AppData\Claude"

# Copy the config file
Copy-Item "configs\config.json" "$env:AppData\Claude\claude_desktop_config.json"

# Open and edit the config file with your preferred text editor
# For example, using VS Code:
code $env:AppData\Claude\claude_desktop_config.json
# Or using Notepad:
notepad $env:AppData\Claude\claude_desktop_config.json
```

Make sure to update the configuration file as described in Step 1. For troubleshooting and common issues, see the [Debugging](#debugging) section at the bottom of this document.

## Configuration Components

Let's break down each part of the configuration:

1. **mcpServers**: The top-level object that contains all MCP server configurations
   - Each server is identified by a unique key (in this case, "waii")

2. **Server Configuration**:
   - `command`: The command to use to start the server (in this case, "/ABSOLUTE/PATH/TO/uv")
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

4. **uv Connection Errors**:
   - If you encounter an ENOENT error when trying to start the server, this likely means Claude cannot find the `uv` executable
   - To fix this, you need to use the full path to the `uv` executable in the `command` field (e.g., `/usr/local/bin/uv` or `C:\path\to\uv.exe`).
   - You can get the full path by running:
     - On MacOS/Linux: `which uv`
     - On Windows: `where uv`
   - Replace `"command": "uv"` with the full path (e.g., `"command": "/usr/local/bin/uv"`)

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

## Debugging

If you encounter issues with your configuration or server setup, try the following troubleshooting steps:

### UV Connection Error
If you encounter a `uv` connection error (error message ENOENT), you may need to use the full path to the `uv` executable in the `command` field. You can get this by running:
- On MacOS/Linux: `which uv`
- On Windows: `where uv`

Copy the output path and replace `"command": "uv"` with the full path (e.g., `"command": "/usr/local/bin/uv"`).
This often happens when installing uv on MacOS/Linux with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Python Version Issues
If you encounter issues with Python version compatibility when using `uv`, follow these steps:

1. Check the current Python version in your project:
   ```bash
   cat .python-version
   ```
   This file is created by `uv init` and specifies the Python version for your project.

2. To set a specific Python version, you have three options:

   a. During project initialization:
   ```bash
   uv init waii-mcp-hands-on-lab --python 3.10
   ```

   b. Or modify the existing setup:
   ```bash
   # Edit .python-version file to set desired version
   echo "3.10" > .python-version
   ```

   c. Using pyenv (recommended for managing multiple Python versions):
   ```bash
   # Install pyenv if not already installed
   # macOS:
   brew install pyenv
   # Linux:
   curl https://pyenv.run | bash

   # Install Python 3.10
   pyenv install 3.10

   # Set local Python version for the project
   pyenv local 3.10
   ```

3. After setting the correct version, recreate the virtual environment and continue with the installation steps.
   ```bash
   # Recreate virtual environment
   deactivate  # if venv is active
   rm -rf .venv
   uv venv
   ```

### API Key Issues
- Make sure you have replaced `<fill in your api key>` in the config file with your actual WAII API key.
- Double-check for typos or extra spaces.
- Do not commit your API key to version control.

### Permissions Issues
- Ensure you have write permissions to the config directory (e.g., `~/Library/Application Support/Claude` on Mac or `%AppData%\Claude` on Windows).
- If you get a permissions error, try running your editor or terminal as an administrator.

For more detailed information about the configuration file, see the rest of this document or reach out to your instructor/support channel.
