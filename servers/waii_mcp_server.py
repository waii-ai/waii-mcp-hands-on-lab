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

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Movie Database Query Generator')
    parser.add_argument('--api-key', required=True, help='WAII API key')
    args = parser.parse_args()

    # Initialize FastMCP server
    mcp = FastMCP("waii") 
    
    # Initialize chatbot
    chatbot = Chatbot(WAII_URL, args.api_key, DATABASE_KEY)

    @mcp.tool(
        name="movie_db_query_generator",
        description="Generate and run SQL queries for the movies and tv database based on natural language questions. Includes information about genres, directors, actors, awards, keywords, finances, and more."
    )
    async def movie_db_query_generator(query: str) -> str:
        """Generate SQL queries for the movies and tv database based on natural language questions.

        Args:
            query: Natural language question about the movie and tv database (e.g. 'Show me all movies from 2023', 
                  'What are the top rated tv shows?', 'List movies directed by Christopher Nolan')
        """
        return chatbot.ask_question(query)

    # Start the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
