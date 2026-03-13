from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import analyze, runs
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Curriculum Gap Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(runs.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "curriculum_analyzer"}
