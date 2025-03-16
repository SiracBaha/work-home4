import json
from jsonschema import validate
from gemini_api import sql_chat, response_chat
from database import execute_query

# Schema for validating the SQL query response
sql_schema = {
    "type": "object",
    "properties": {
        "sqlQuery": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["sqlQuery"],  
}

response_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
    },
    "required": ["message"],
}

def extract_json_from_response(text):
    """Extract JSON from model response, handling different formats."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            if '```json' in text:
                json_text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                json_text = text.split('```')[1].split('```')[0]
            else:
                json_text = text
            json_text = json_text.strip()
            return json.loads(json_text)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Raw text: {text}")
            raise

def ask(question, history):
    """Process the question using two different models."""
    try:
        # Step 1: Generate SQL query using Gemini Pro 1.5
        sql_result = sql_chat.send_message(
            f"Generate a SQL query for this question: {question}\nRespond only with a JSON object in the specified format."
        )
        
        sql_json = extract_json_from_response(sql_result.text)
        validate(instance=sql_json, schema=sql_schema)
        
        # Extract the query correctly
        query = sql_json["sqlQuery"]  

        # Execute the generated SQL query
        data = execute_query(query)
        dataText = json.dumps(data)

        # Step 2: Generate response using Gemini Flash 2.0
        response_result = response_chat.send_message(
            f"The question of the user was: {question}.\n\n ----- \n\n The result of the query is: {dataText}\n\n ---- \n\n Now give user a pretty message in the specified JSON format."
        )
        
        response_json = extract_json_from_response(response_result.text)
        validate(instance=response_json, schema=response_schema)

        return response_json["message"]

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"
