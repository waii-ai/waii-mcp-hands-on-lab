# Build a MCP Server

In this section, we'll build an MCP server that uses WAII to generate SQL queries from natural language questions. We'll break down the implementation into clear steps.
You can follow along by creating a new file called `my_waii_mcp_server.py` in the servers directory.

## Prerequisites
Before proceeding with the implementation, please ensure you have completed all the installation steps in the [Prerequisites and Setup Instructions](../PREREQUISITES.md) section.

## Step 1: Create the Chatbot Class

First, let's create the Chatbot class that will handle WAII integration. 

```python
from waii_sdk_py import WAII
from waii_sdk_py.chat import ChatRequest, ChatModule

class Chatbot:
    def __init__(self, url: str, api_key: str, database_key: str):
        print(f"Initializing WAII client with URL: {url}")
        # Initialize WAII client
        WAII.initialize(
            api_key=api_key,
            url=url,
        )
        print("Activating database connection...")
        WAII.database.activate_connection(database_key)
        print("Database connection activated successfully")
        
        self.previous_chat_uuid = None
        self.enabled_chat_modules = [
            ChatModule.CONTEXT,
            ChatModule.TABLES,
            ChatModule.QUERY,
            ChatModule.DATA
        ]

    def ask_question(self, message: str) -> str:
        chat_response = WAII.chat.chat_message(ChatRequest(
            ask=message,
            parent_uuid=self.previous_chat_uuid,
            modules=self.enabled_chat_modules,
        ))
        self.previous_chat_uuid = chat_response.chat_uuid
        response = process_response(chat_response)
        return response
```

## Step 2: Create the Main Function

Now, let's create the main function that will handle command-line arguments and initialize our server:

```python
import argparse

# Constants
WAII_URL = "https://sql.dev.waii.ai/api/"
DATABASE_KEY = "snowflake://WAII_USER@gqobxjv-bhb91428/MOVIE_DB?role=WAII_USER_ROLE&warehouse=COMPUTE_WH"

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Movie Database Query Generator')
    parser.add_argument('--api-key', required=True, help='WAII API key')
    args = parser.parse_args()

    # Initialize chatbot
    chatbot = Chatbot(WAII_URL, args.api_key, DATABASE_KEY)
```

## Step 3: Set Up MCP Infrastructure

Let's add the MCP server setup to our main function:

```python
from mcp.server import FastMCP

def main():
    # ... previous code ...

    # Initialize FastMCP server
    mcp = FastMCP("waii")
```

## Step 4: Create the MCP Tool

Now, let's create our MCP tool with proper documentation:

```python
def main():
    # ... previous code ...

    # Declare the mcp tool for Claude to use to talk to the database
    @mcp.tool(
        name="movie_db_query_generator",
        description="Generate and run SQL queries for the movie database based on natural language questions. Includes information about genres, directors, actors, awards, keywords, finances, and more."
    )
    async def movie_db_query_generator(query: str) -> str:
        """Generate SQL queries for the movie database based on natural language questions.

        Args:
            query: Natural language question about the movie database (e.g. "Show me all movies from 2023", 
                  "What are the top rated action movies?", "List movies directed by Christopher Nolan")
        """
        return chatbot.ask_question(query)

    # Start the server
    mcp.run(transport='stdio')
```

## Step 5: Add Exception Handling

Now, let's add proper exception handling to make our server more robust. We'll need to add these imports at the top of the file:

```python
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS
```

Then, let's update our Chatbot class with exception handling:

```python
class Chatbot:
    def __init__(self, url: str, api_key: str, database_key: str):
        try:
            print(f"Initializing WAII client with URL: {url}")
            # Initialize WAII client
            WAII.initialize(
                api_key=api_key,
                url=url,
            )
            print("Activating database connection...")
            WAII.database.activate_connection(database_key)
            print("Database connection activated successfully")
        except Exception as e:
            error_msg = f"Failed to initialize WAII client: {str(e)}"
            print(f"ERROR: {error_msg}")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))
        
        self.previous_chat_uuid = None
        self.enabled_chat_modules = [
            ChatModule.CONTEXT,
            ChatModule.TABLES,
            ChatModule.QUERY,
            ChatModule.DATA
        ]

    def ask_question(self, message: str) -> str:
        try:
            chat_response = WAII.chat.chat_message(ChatRequest(
                ask=message,
                parent_uuid=self.previous_chat_uuid,
                modules=self.enabled_chat_modules,
            ))
            self.previous_chat_uuid = chat_response.chat_uuid
            response = process_response(chat_response)
            return response
        except Exception as e:
            error_msg = f"Error asking question: {str(e)}"
            raise McpError(ErrorData(code=INVALID_PARAMS, message=error_msg))
```

The exception handling provides:
1. In the `__init__` method:
   - Try-catch block for WAII initialization
   - Error handling for database connection
   - Custom error messages with McpError

2. In the `ask_question` method:
   - Try-catch block for chat message processing
   - Error handling for response processing
   - Custom error messages with McpError

## Complete Implementation

Here's how all the pieces fit together:

```python
from mcp.shared.exceptions import McpError
from mcp.server import FastMCP
from mcp.types import ErrorData, INVALID_PARAMS
from waii_sdk_py import WAII
from waii_sdk_py.chat import ChatRequest, ChatModule
import argparse
from utils import process_response

# Constants
WAII_URL = "https://sql.dev.waii.ai/api/"
DATABASE_KEY = "snowflake://WAII_USER@gqobxjv-bhb91428/MOVIE_DB?role=WAII_USER_ROLE&warehouse=COMPUTE_WH"

class Chatbot:
    # ... Chatbot implementation from Step 5 ...

def main():
    # ... Main function implementation from Steps 2-4 ...

if __name__ == "__main__":
    main()
```

## Configuration

Now that we've verified the server works, we need to configure Claude to use it. The configuration is necessary because:
1. It tells Claude how to start your MCP server
2. It specifies the command to run and any required arguments
3. It ensures Claude can properly communicate with your server

For detailed information about setting up the configuration file, see [MCP Server Configuration](config_file.md).

## Testing with Claude

Now that your server is configured, you can test it with Claude:

1. Start Claude Desktop
2. Try these example questions:
   ```
   How can I calculate the total number of movies in the database?
   ```
   ```
   How can I calculate the number of movies per genre in each decade? Get me a query for this.
   ```

These questions will help verify that your MCP server is working correctly with Claude.

