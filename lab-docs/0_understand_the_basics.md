# Understanding the Basics of MCP Server

## What is MCP?

MCP (Model Control Protocol) is a protocol that enables AI models to interact with external tools and services. It provides a standardized way for AI models to declare, discover, and use tools, making it easier to extend AI capabilities with custom functionality.

## MCP Components: Clients and Server Relationship

The MCP ecosystem consists of three main components:

1. **MCP Server**: The central component that manages tool declarations and handles requests from clients. It acts as a bridge between AI models and external tools.

2. **MCP Clients**: These are AI models or applications that want to use the tools declared by the server. Clients connect to the server to discover available tools and make requests to use them.

3. **Tools**: The actual implementations of functionality that can be used by clients. Tools are declared to the MCP server and can perform various operations like database queries, API calls, or custom business logic.

## Using the MCP Library and Tool Declaration

To use MCP in your project:

1. **Install the MCP Library**: The MCP library provides the necessary components to create and manage an MCP server. Here's how to initialize and run an MCP server:

```python
from mcp.server import FastMCP

# Initialize FastMCP server with a unique identifier
mcp = FastMCP("waii")

# ... tool declarations ...

# Start the server using stdio transport
mcp.run(transport='stdio')
```

2. **Declare Tools**: Tools are declared using a specific format that includes:
   - Tool name and description
   - Input parameters and their types
   - Output format
   - Implementation details

The docstring and the tool declaration are crucial as it provides the interface documentation for AI models. They should include:
- A clear description of what the tool does
- Args section describing each parameter
- Example usage in the description

Here's an example of how to declare a tool using the MCP library:

```python
@mcp.tool(
    name="movie_db_query_generator",
    description="Generate SQL queries for the movie database based on natural language questions. Includes information about genres, directors, actors, awards, keywords, finances, and more."
)
async def movie_db_query_generator(query: str) -> str:
    """Generate SQL queries for the movie database based on natural language questions.

    Args:
        query: Natural language question about the movie database (e.g. "Show me all movies from 2023", 
              "What are the top rated action movies?", "List movies directed by Christopher Nolan")
    """
    # ... implementation
```

3. **Register Tools**: Once declared, tools need to be registered with the MCP server to make them available to clients.

## WAII Integration for Database Communication

In this lab, we'll use WAII to power our tools and enable database communication:

1. **WAII Integration**: WAII provides natural language to SQL capabilities, allowing tools to communicate with databases using natural language queries.

2. **Tool Implementation**: We'll implement tools that use WAII to:
   - Convert natural language queries to SQL
   - Execute database operations
   - Return results in a structured format

Here's how we implement the WAII integration:

```python
class Chatbot:
    def __init__(self, url: str, api_key: str, database_key: str):
        # Initialize WAII client
        WAII.initialize(
            api_key=api_key,
            url=url,
        )
        # Activate database connection
        WAII.database.activate_connection(database_key)
        # ... 

    # Called by MCP tool implementation
    def ask_question(self, message: str) -> str:
        chat_response = WAII.chat.chat_message(ChatRequest(
            ask=message,
        ))
        # ...
        return chat_response
```

## MCP Configuration

The MCP server requires a configuration file to tell Claude how to start and connect to your server. For detailed information about the configuration file, see [MCP Server Configuration](config_file.md).

In the next sections, we'll learn how to implement these concepts and build a working MCP server with WAII integration.
