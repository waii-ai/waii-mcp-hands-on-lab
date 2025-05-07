from mcp.shared.exceptions import McpError
from mcp.server import FastMCP
from mcp.types import (
    ErrorData,
    INVALID_PARAMS,
)
from waii_sdk_py import WAII
from waii_sdk_py.chat import ChatRequest, ChatModule, ChatResponse
from waii_sdk_py.query import GetQueryResultResponse
from io import StringIO
import argparse

# Constants
WAII_URL = 'http://internal-testing.dev.waii.ai/api/'
DATABASE_KEY = "snowflake://WAII_USER@gqobxjv-bhb91428/MOVIE_DB?role=WAII_USER_ROLE&warehouse=COMPUTE_WH"  # Hardcoded database key

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
        ]

    @staticmethod
    def serialize_query_result_response(response: GetQueryResultResponse, limit=10):
        try:
            df = response.to_pandas_df()
            output = StringIO()
            df.head(limit).to_csv(output, index=False)
            csv_string = output.getvalue().strip()

            # Truncate long lines
            lines = csv_string.split('\n')
            truncated_lines = []
            for line in lines:
                if len(line) > 500:
                    truncated_lines.append(line[:497] + '...')
                else:
                    truncated_lines.append(line)
            csv_string = '\n'.join(truncated_lines)

            if len(df) > limit:
                csv_string += "\n..."

            # if the csv string is too long (5k), truncate it
            if len(csv_string) > 5000:
                csv_string = csv_string[:5000] + "..."

            csv_string += f"\n--\n{len(df)} row(s)"
            return csv_string
        except Exception as e:
            error_msg = f"Error serializing query result: {str(e)}"
            return f"Error processing results: {error_msg}"

    @staticmethod
    def process_response(chat_response: ChatResponse):
        try:
            references_section = ""
            if "<query>" in chat_response.response:
                references_section += f"Generated query:\n```\n{chat_response.response_data.query.query}\n```\n"
            if "<data>" in chat_response.response:
                references_section += f"Data:\n{Chatbot.serialize_query_result_response(chat_response.response_data.data, limit=100)}\n"
            return chat_response.response + "\n" + references_section
        except Exception as e:
            error_msg = f"Error processing chat response: {str(e)}"
            return f"Error processing response: {error_msg}"

    def ask_question(self, message: str) -> str:
        try:
            chat_response = WAII.chat.chat_message(ChatRequest(
                ask=message,
                parent_uuid=self.previous_chat_uuid,
                modules=self.enabled_chat_modules,
            ))
            self.previous_chat_uuid = chat_response.chat_uuid
            response = self.process_response(chat_response)
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

    @mcp.tool(name="movie_db_query_generator",
              description="Talk to attached movie database and generate queries to show to the user.")
    async def movie_db_query_generator(query: str) -> str:
        """Generate SQL queries for the movie database based on natural language questions.

        Args:
            query: Natural language question about the movie database (e.g. "Show me all movies from 2023", 
                  "What are the top rated action movies?", "List movies directed by Christopher Nolan")
        """
        return chatbot.ask_question(query)

    # Start the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
