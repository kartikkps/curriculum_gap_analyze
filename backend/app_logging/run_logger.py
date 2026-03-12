import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("curriculum_analyzer")
logger.setLevel(logging.INFO)

log_file_path = Path("runs.jsonl")

if not log_file_path.exists():
    log_file_path.touch()

file_handler = logging.FileHandler(log_file_path)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage()
        }
        if hasattr(record, "run_id"):
            log_record["run_id"] = record.run_id
        if hasattr(record, "agent_name"):
            log_record["agent_name"] = record.agent_name
        if hasattr(record, "event_type"):
            log_record["event_type"] = record.event_type
        if hasattr(record, "details"):
            log_record["details"] = record.details
        return json.dumps(log_record)

file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

def log_state_transition(run_id: str, agent_name: str, previous_state: str, event: str, next_state: str):
    logger.info(
        f"State transition: {previous_state} -> {next_state}",
        extra={
            "run_id": run_id,
            "agent_name": agent_name,
            "event_type": "state_transition",
            "details": {
                "previous_state": previous_state,
                "event": event,
                "next_state": next_state
            }
        }
    )

def log_tool_call(run_id: str, agent_name: str, tool_name: str, tool_inputs: dict, tool_outputs: dict):
    logger.info(
        f"Tool call: {tool_name}",
        extra={
            "run_id": run_id,
            "agent_name": agent_name,
            "event_type": "tool_call",
            "details": {
                "tool_name": tool_name,
                "tool_inputs": tool_inputs,
                "tool_outputs": tool_outputs
            }
        }
    )
