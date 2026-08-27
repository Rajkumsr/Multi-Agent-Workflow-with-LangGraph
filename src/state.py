from typing import TypedDict, Annotated, Optional
import operator

class AgentState(TypedDict):
    """
    State schema for the Multi-Agent Workflow.
    """
    task: str
    plan: Optional[str]
    draft: Optional[str]
    feedback: Optional[str]
    status: str # 'pending', 'working', 'reviewing', 'approved', 'failed'
    rejection_count: Annotated[int, operator.add]
