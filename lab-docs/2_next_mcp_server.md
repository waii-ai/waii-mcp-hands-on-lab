# Allow MCP Server to Run Queries

Now that you know how to build a basic MCP server, let's enhance it to handle data queries. We'll modify the existing server to add data querying capabilities.

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
    @mcp.tool()
    async def movie_db_query_generator(query: str) -> str:
        """Generate and run SQL queries for the movies and tv database based on natural language questions. Includes information about genres, directors, actors, awards, keywords, finances, and more.
    ...
```

## Step 2: Test the Changes

To test the enhanced server:

1. Stop the Claude Desktop application
2. Restart Claude Desktop
3. Try asking a data-related question, for example:
   - "How many movies have won Oscars?"
   - "How many movies have been per genre"

The server will now be able to handle data queries and return structured results.

## What Changed?

By adding `ChatModule.DATA` to the enabled modules, we've given the server the ability to:
- Execute data queries
- Return structured data results

The server will now process these queries through WAII's data module, which can handle both SQL generation and data processing.

## Testing with Claude

Now that your server is enhanced with data querying capabilities, you can test it with Claude by asking this question:

```
How many comedy movies were created each decade?
```

When you ask this question, Claude will use the MCP server to generate the appropriate SQL query and process the data through WAII's data module to provide you with a detailed breakdown of comedy movies by decade.
