schema={
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
        "description": "The category of the question (e.g., 'command-line', 'file-processing', 'web', 'data-manipulation', 'llm-task').",
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
        "description": "Optional file attachments relevant to the question. Each attachment should include a filename and its content.",
        "items": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string",
              "description": "The name of the file attachment."
            },
            "content": {
              "type": "string",
              "description": "The file content (if binary, it should be base64 encoded)."
            }
          },
          "required": ["filename", "content"]
        }
      }
    },
    "required": ["question"]
  },
  "response": {
    "type": "object",
    "properties": {
      "answer": {
        "type": "string",
        "description": "A single concise answer to the provided assignment question."
      }
    },
    "required": ["answer"]
  }
}


system_prompt= '''
You are an AI assistant designed to answer graded assignment questions. Each question comes with an optional 'category' field:
- For "command-line" questions, focus on command outputs.
- For "file-processing" questions, process file data and extract the necessary information.
- For "web" questions, perform the necessary HTTP requests.
- For "data-manipulation" tasks, compute or parse data as needed.
- For "llm-task" questions, perform advanced language model operations.
Return only the final answer in a concise format.

'''