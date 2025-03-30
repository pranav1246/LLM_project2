import openai
import json
import os
from dotenv import load_dotenv

load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

api_key = os.getenv("OPENAI_API_KEY")

# Define the function schema
function_schema = {
    "name": "assignment_answering_tool",
    "description": "Processes an assignment question with optional file attachments and returns a single concise answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The assignment question text that needs to be answered."
            },
            "category": {
                "type": "string",
                "description": "The category of the question (e.g., 'command-line', 'file-processing', 'web', 'data-manipulation', 'llm-task', or 'other').",
                "enum": [
                    "command-line",
                    "file-processing",
                    "web",
                    "data-manipulation",
                    "llm-task",
                    "other"
                ]
            },
            "attachments": {
                "type": "array",
                "description": "Optional file attachments relevant to the question.",
                "items": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["filename", "content"]
                }
            }
        },
        "required": ["question"]
    }
}

system_prompt = (
    "You are an AI assistant that answers graded assignment questions accurately and concisely. "
    "Return only the final answer with no extra text."
)

def get_llm_answer(question: str) -> str:
   
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": question}],
        functions=[function_schema],
        function_call={"name": "assignment_answering_tool"},
        temperature=0.1,
        max_tokens=100
    )

    function_call_arguments = response["choices"][0]["message"]["function_call"]["arguments"]
    parsed_arguments = json.loads(function_call_arguments)
    return parsed_arguments.get("answer", "No answer found.")
