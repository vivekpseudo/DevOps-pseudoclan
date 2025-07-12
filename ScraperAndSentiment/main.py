from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import subprocess
import json

from transformers import pipeline
from tone_predictor import predict_tones
from response_generator import generate_admin_response

# Initialize FastAPI app
app = FastAPI()

# Load HuggingFace pipelines
qa_pipeline = pipeline("question-answering")
sentiment_pipeline = pipeline("sentiment-analysis")

# --------------------------
# Pydantic Schemas
# --------------------------
class ReviewInput(BaseModel):
    reviews: List[str]

class QARequest(BaseModel):
    question: str
    context: str

class ReviewPrediction(BaseModel):
    review: str
    sentiment_scores: Dict[str, float]
    tones: Dict[str, float]

# --------------------------
# Root & Health
# --------------------------
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the unified API.",
        "endpoints": ["/scrape (GET)", "/predict (POST)", "/generate_response (POST)", "/qa (POST)", "/health (GET)"],
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --------------------------
# Scraper Endpoint
# --------------------------
@app.get("/scrape")
def scrape_data(query: str = Query(...), city: str = Query(...)):
    """Scrapes info for a given query and city using external scraper.py."""
    try:
        result = subprocess.run(
            ["python", "scraper.py", query, city],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return {"error": f"Scraper failed: {result.stderr.strip()}"}

        output = result.stdout.strip()

        try:
            info = json.loads(output)
            return {"businesses": info}
        except json.JSONDecodeError:
            return {"error": "Invalid scraper output", "raw_output": output}

    except subprocess.TimeoutExpired:
        return {"error": "Scraper timed out"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# --------------------------
# Tone/Sentiment Prediction
# --------------------------
@app.post("/predict")
def predict_tone(input: ReviewInput):
    try:
        predictions = predict_tones(input.reviews)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------
# Admin Response Generation
# --------------------------
@app.post("/generate_response")
def get_generated_response(data: ReviewPrediction):
    try:
        result = generate_admin_response(data.review, data.sentiment_scores, data.tones)
        return {"admin_responses": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------
# Question Answering
# --------------------------
@app.post("/qa")
def get_answer(payload: QARequest):
    try:
        result = qa_pipeline(question=payload.question, context=payload.context)
        return {"answer": result["answer"], "score": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
