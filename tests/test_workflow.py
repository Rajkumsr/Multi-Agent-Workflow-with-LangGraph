from src.graph import build_graph

def test_graph_initialization():
    graph = build_graph()
    assert graph is not None
    
def test_workflow_rejection_logic():
    graph = build_graph()
    
    initial_state = {
        "task": "Test task",
        "plan": None,
        "draft": None,
        "feedback": None,
        "status": "pending",
        "rejection_count": 0
    }
    
    events = list(graph.stream(initial_state))
    
    # In our mock logic, it gets rejected twice, and stops.
    # We can count the number of times it visits the reviewer node.
    reviewer_visits = sum(1 for event in events if "reviewer" in event)
    
    # 1st try: count=0 -> rejected (returns count=1) -> routes to worker
    # 2nd try: count=1 -> rejected (returns count=1) -> routes to end (MAX REJECTIONS REACHED)
    assert reviewer_visits == 2
