import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import build_graph
def run_workflow():
    print("Starting Multi-Agent Workflow...\n")
    graph = build_graph()
    
    initial_state = {
        "task": "Write a short blog post about AI Agents.",
        "plan": None,
        "draft": None,
        "feedback": None,
        "status": "pending",
        "rejection_count": 0
    }
    
    # Run the graph
    for event in graph.stream(initial_state):
        for node_name, node_state in event.items():
            print(f"--- Finished node: {node_name} ---")
            # print(f"Current State: {node_state}\n")
    
    print("\nWorkflow Completed!")
    
if __name__ == "__main__":
    run_workflow()
