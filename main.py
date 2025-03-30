from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
import os
import shutil
from llm_handler import get_llm_answer


app = FastAPI()

class AnswerResponse(BaseModel):
    answer: str

@app.post("/api/", response_model=AnswerResponse)
async def get_answer(question: str = Form(...), file: UploadFile = File(None)):
    """
    API endpoint to accept a question and an optional file, then return an answer.
    """
    if file:
        file_location = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Fetch answer from LLM
    answer = get_llm_answer(question)

    return {"answer": answer}
