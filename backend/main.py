from fastapi import FastAPI
from api import analyze, runs
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Curriculum Gap Analyzer API")

app.include_router(analyze.router)
app.include_router(runs.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "curriculum_analyzer"}
