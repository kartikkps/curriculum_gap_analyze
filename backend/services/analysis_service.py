import uuid
import json
from sqlalchemy.orm import Session
from database import RunModel, AnalysisModel
from agents.gap_agent import GapAnalyzerAgent
from models.analysis import GapAnalysisResult
from typing import Dict, Any

def run_analysis_service(db: Session, target_curr: str, student_curr: str, seed: int = 42) -> Dict[str, Any]:
    run_id = str(uuid.uuid4())
    db_run = RunModel(id=run_id, seed=seed, status="RUNNING")
    db.add(db_run)
    db.commit()
    agent = GapAnalyzerAgent(run_id=run_id)
    try:
        agent.run(target_curr, student_curr)
        db_run.status = "COMPLETED"
        db.commit()
        analysis = AnalysisModel(
            run_id=run_id,
            gap_score=agent.metrics.get("gap_score", 0.0),
            coverage_percentage=agent.metrics.get("coverage_percentage", 0.0),
            topic_similarity_score=agent.metrics.get("topic_similarity_score", 0.0),
            result_json=agent.gap_result.model_dump_json() if agent.gap_result else "{}"
        )
        db.add(analysis)
        db.commit()
        return {
            "run_id": run_id,
            "status": "COMPLETED",
            "metrics": agent.metrics,
            "result": agent.gap_result.model_dump() if agent.gap_result else {}
        }
    except Exception as e:
        db_run.status = "FAILED"
        db.commit()
        raise e
