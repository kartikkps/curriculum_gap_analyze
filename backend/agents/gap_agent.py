import time
from typing import Dict, Any
from state_machine.workflow import WorkflowStateMachine
from state_machine.states import State
from tools.syllabus_parser import parse_syllabus
from tools.similarity_tool import calculate_similarity
from tools.gap_detector import detect_gaps
from app_logging.run_logger import log_tool_call
from models.analysis import GapAnalysisResult
from models.curriculum import Curriculum

class GapAnalyzerAgent:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.name = "GapAnalyzerAgent"
        self.workflow = WorkflowStateMachine(run_id=run_id, agent_name=self.name)
        self.max_steps = 10
        self.tool_timeout = 5
        self.target_text = ""
        self.student_text = ""
        self.target_curriculum: Curriculum = None
        self.student_curriculum: Curriculum = None
        self.gap_result: GapAnalysisResult = None
        self.metrics: Dict[str, float] = {}

    def run(self, target_curriculum_text: str, student_curriculum_text: str) -> None:
        self.target_text = target_curriculum_text
        self.student_text = student_curriculum_text
        step = 0
        while self.workflow.current_state != State.COMPLETED and step < self.max_steps:
            self._step()
            step += 1
        if step >= self.max_steps and self.workflow.current_state != State.COMPLETED:
            raise Exception("Agent exceeded max steps without completing.")

    def _step(self):
        state = self.workflow.current_state
        if state == State.IDLE:
            self.workflow.transition_to(State.UPLOAD_SYLLABUS, event="start_processing")
        elif state == State.UPLOAD_SYLLABUS:
            self.workflow.transition_to(State.PROCESS_SYLLABUS, event="syllabuses_received")
        elif state == State.PROCESS_SYLLABUS:
            self.target_curriculum = self._run_tool_with_timeout(
                "parse_syllabus", parse_syllabus, {"text": self.target_text}
            )
            self.student_curriculum = self._run_tool_with_timeout(
                "parse_syllabus", parse_syllabus, {"text": self.student_text}
            )
            self.workflow.transition_to(State.COMPARE_CURRICULUM, event="parsing_complete")
        elif state == State.COMPARE_CURRICULUM:
            similarity_score = self._run_tool_with_timeout(
                "calculate_similarity",
                calculate_similarity,
                {"target": self.target_curriculum, "student": self.student_curriculum}
            )
            self.metrics["topic_similarity_score"] = similarity_score
            self.workflow.transition_to(State.IDENTIFY_GAPS, event="comparison_complete")
        elif state == State.IDENTIFY_GAPS:
            missing, weak, gap_score = self._run_tool_with_timeout(
                "detect_gaps",
                detect_gaps,
                {"target": self.target_curriculum, "student": self.student_curriculum}
            )
            self.metrics["gap_score"] = gap_score
            coverage = (1.0 - gap_score) * 100
            self.metrics["coverage_percentage"] = coverage
            learning_order = [m.topic_name for m in missing] + weak
            self.gap_result = GapAnalysisResult(
                missing_topics=missing,
                weak_topics=weak,
                recommended_learning_order=learning_order,
                gap_score=gap_score
            )
            self.workflow.transition_to(State.GENERATE_REPORT, event="gaps_identified")
        elif state == State.GENERATE_REPORT:
            self.workflow.transition_to(State.COMPLETED, event="report_generated")

    def _run_tool_with_timeout(self, tool_name: str, func, kwargs: Dict[str, Any]):
        start_time = time.time()
        log_tool_call(self.run_id, self.name, tool_name, {k: str(v)[:100] for k,v in kwargs.items()}, {})
        try:
            result = func(**kwargs)
            duration = time.time() - start_time
            if duration > self.tool_timeout:
                raise TimeoutError(f"Tool {tool_name} exceeded timeout of {self.tool_timeout}s")
            log_tool_call(self.run_id, self.name, tool_name, {k: str(v)[:100] for k,v in kwargs.items()}, {"status": "success"})
            return result
        except Exception as e:
            log_tool_call(self.run_id, self.name, tool_name, {k: str(v)[:100] for k,v in kwargs.items()}, {"error": str(e)})
            raise
