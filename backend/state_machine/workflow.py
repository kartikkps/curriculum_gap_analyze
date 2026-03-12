from state_machine.states import State
from app_logging.run_logger import log_state_transition

class WorkflowStateMachine:
    def __init__(self, run_id: str, agent_name: str, initial_state: State = State.IDLE):
        self.run_id = run_id
        self.agent_name = agent_name
        self.current_state = initial_state

    def transition_to(self, next_state: State, event: str = "auto_transition"):
        previous_state = self.current_state
        self.current_state = next_state
        log_state_transition(
            run_id=self.run_id,
            agent_name=self.agent_name,
            previous_state=previous_state.value,
            event=event,
            next_state=next_state.value
        )
