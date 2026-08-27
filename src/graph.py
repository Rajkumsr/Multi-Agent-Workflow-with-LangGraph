# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import planner_node, worker_node, reviewer_node

def should_continue(state: AgentState):
    """
    Conditional edge function to determine the next step after review.
    """
    status = state.get("status")
    rejection_count = state.get("rejection_count", 0)
    
    if status == "approved":
        return "end"
    elif status == "failed":
        if rejection_count >= 2:
            print("MAX REJECTIONS REACHED. Stopping workflow.")
            return "end"
        else:
            return "continue"
            
    return "end"

def build_graph():
    """
    Constructs and compiles the multi-agent workflow graph.
    """
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("planner", planner_node)
    builder.add_node("worker", worker_node)
    builder.add_node("reviewer", reviewer_node)
    
    # Add edges
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "worker")
    builder.add_edge("worker", "reviewer")
    
    # Add conditional edge from reviewer
    builder.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "continue": "worker",
            "end": END
        }
    )
    
    # Compile the graph
    graph = builder.compile()
    return graph
