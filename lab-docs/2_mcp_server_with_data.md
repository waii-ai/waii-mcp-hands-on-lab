# Allow MCP Server to Run Queries

Now that you know how to build a basic MCP server, let's enhance it to handle data as well. We'll modify the existing server to add data querying capabilities.
This is already implemented in `server/waii_mcp_server_with_data.py` if you want to skip the coding (please still see prerequisites)

## Prerequisites

Before we proceed, make sure you have pandas installed:

```bash
uv pip install pandas
```

This is required for data processing capabilities in the WAII integration.

## Step 1: Update the Chatbot Class

In your `waii_mcp_server.py`, we'll add the DATA module to the enabled modules list. Here's how to modify the Chatbot class:

```python
class Chatbot:
    def __init__(self, url: str, api_key: str, database_key: str):
        # ... previous code
        self.enabled_chat_modules = [
            ChatModule.CONTEXT,
            ChatModule.TABLES,
            ChatModule.QUERY,
            ChatModule.DATA  # Add this line to enable data querying
        ]
```

Also, update the tool description to inform Claude about the query execution capabilities:
```python
    @mcp.tool(
        name="movie_db_query_generator",
        description="Generate and run SQL queries for the movies and tv database based on natural language questions. Includes information about genres, directors, actors, awards, keywords, finances, and more. This version also executes the queries and returns the actual data results."
    )
    async def movie_db_query_generator(query: str) -> str:
        # ... implementation
```

## Step 2: Test the Changes

To test the enhanced server:

1. Stop the Claude Desktop application
2. Optional, update the config if using a new file
3. Restart Claude Desktop
4. Try asking a data-related question, for example:
   - "How many movies have won Oscars?"
   - "How many movies per genre"

The server will now be able to handle data queries and return structured results.

## What Changed?

By adding `ChatModule.DATA` to the enabled modules, we've given the server the ability to:
- Execute data queries
- Return structured data results (note row length limited to 100 rows)

The server will now process these queries through WAII's data module, which can handle both SQL generation and data processing.