from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Load the HuggingFace QA model
qa_pipeline = pipeline("question-answering")

# Input schema
class QARequest(BaseModel):
    question: str
    context: str

# Define endpoint
@app.post("/qa")
def get_answer(payload: QARequest):
    try:
        result = qa_pipeline(question=payload.question, context=payload.context)
        return {"answer": result["answer"], "score": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
