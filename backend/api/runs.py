from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

@router.get("/runs/{run_id}")
def get_run_logs(run_id: str):
    log_file_path = Path("runs.jsonl")
    if not log_file_path.exists():
        raise HTTPException(status_code=404, detail="Logs not found")
    run_logs = []
    with open(log_file_path, 'r') as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                if log_entry.get("run_id") == run_id:
                    run_logs.append(log_entry)
            except json.JSONDecodeError:
                continue
    if not run_logs:
        raise HTTPException(status_code=404, detail=f"No logs found for run_id {run_id}")
    return {"run_id": run_id, "logs": run_logs}
