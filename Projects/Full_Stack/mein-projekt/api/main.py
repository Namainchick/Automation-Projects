from fastapi import FastAPI
from pydantic import BaseModel
from mycore.service import add, analyze

app = FastAPI(title="My API")

class AddIn(BaseModel):
    a: float
    b: float

class AddOut(BaseModel):
    result: float

class AnalyzeIn(BaseModel):
    text: str

class AnalyzeOut(BaseModel):
    length: int
    upper: str

@app.post("/add", response_model=AddOut)
def add_route(payload: AddIn):
    return AddOut(result=add(payload.a, payload.b))

@app.post("/analyze", response_model=AnalyzeOut)
def analyze_route(payload: AnalyzeIn):
    res = analyze(payload.text)
    return AnalyzeOut(**res)

# CORS (Frontend unter 5173 zulassen)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
