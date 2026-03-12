from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from services.analysis_service import run_analysis_service

router = APIRouter()

class AnalysisRequest(BaseModel):
    target_curriculum: str
    student_curriculum: str
    seed: int = 42

@router.post("/analyze")
def analyze_curriculums(request: AnalysisRequest, db: Session = Depends(get_db)):
    try:
        result = run_analysis_service(
            db=db,
            target_curr=request.target_curriculum,
            student_curr=request.student_curriculum,
            seed=request.seed
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
