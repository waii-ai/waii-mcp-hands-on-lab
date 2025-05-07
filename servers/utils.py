from io import StringIO
from waii_sdk_py.query import GetQueryResultResponse
from waii_sdk_py.chat import ChatResponse

def serialize_query_result_response(response: GetQueryResultResponse, limit=10):
    """Serialize a query result response to a formatted string.
    
    Args:
        response: The query result response to serialize
        limit: Maximum number of rows to include in the output
        
    Returns:
        A formatted string containing the query results
    """
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

def process_response(chat_response: ChatResponse):
    """Process a chat response and format it with any query results.
    
    Args:
        chat_response: The chat response to process
        
    Returns:
        A formatted string containing the response and any query results
    """
    try:
        references_section = ""
        if "<query>" in chat_response.response:
            references_section += f"Generated query:\n```\n{chat_response.response_data.query.query}\n```\n"
        if "<data>" in chat_response.response:
            references_section += f"Data:\n{serialize_query_result_response(chat_response.response_data.data, limit=100)}\n"
        return chat_response.response + "\n" + references_section
    except Exception as e:
        error_msg = f"Error processing chat response: {str(e)}"
        return f"Error processing response: {error_msg}"
