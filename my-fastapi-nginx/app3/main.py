# app1/main.py (also same for app2 and app3 with different message)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from App 3"}
