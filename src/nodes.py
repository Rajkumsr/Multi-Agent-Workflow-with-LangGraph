import os
from typing import Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from .state import AgentState

# Initialize the OpenAI model (Requires OPENAI_API_KEY environment variable)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def planner_node(state: AgentState) -> Dict:
    """The planner node takes the task and creates a plan."""
    print("--- PLANNER ---")
    task = state["task"]
    
    prompt = f"You are a planning assistant. Create a step-by-step plan for the following task:\n\n{task}"
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {"plan": response.content, "status": "working"}

def worker_node(state: AgentState) -> Dict:
    """The worker node executes the plan and generates a draft."""
    print("--- WORKER ---")
    plan = state.get("plan", "")
    feedback = state.get("feedback", "")
    task = state["task"]
    
    if feedback:
        prompt = f"You are a worker. Revise your draft for the task: '{task}'.\n\nPlan: {plan}\n\nReviewer Feedback to address:\n{feedback}\n\nProvide the revised draft."
    else:
        prompt = f"You are a worker. Create an initial draft for the task: '{task}'.\n\nPlan to follow:\n{plan}\n\nProvide the draft."
        
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft": response.content, "status": "reviewing"}

def reviewer_node(state: AgentState) -> Dict:
    """The reviewer node evaluates the draft."""
    print("--- REVIEWER ---")
    draft = state.get("draft", "")
    task = state["task"]
    rejection_count = state.get("rejection_count", 0)
    
    prompt = f"""You are a strict reviewer. Evaluate the draft for the task: '{task}'.
Draft:
{draft}

Your current rejection count is: {rejection_count}.
For the purpose of this demonstration, you MUST be extremely harsh. If the rejection count is less than 2, find a reason to reject the draft and ask for more details. 
If the rejection count is 2 or more, you can choose to approve it if it looks good, or reject it again.

If you approve it, respond with exactly: APPROVED
If it needs work, respond with exactly: REJECTED: <your feedback>"""

    response = llm.invoke([SystemMessage(content=prompt)])
    content = response.content.strip()
    
    if content.startswith("APPROVED"):
        print("Reviewer decision: APPROVED")
        return {"feedback": "", "status": "approved"}
    else:
        feedback = content.replace("REJECTED:", "").strip()
        # For demonstration, if we hit our internal threshold, we force it through the failure path
        print(f"Reviewer decision: REJECTED. Feedback: {feedback}")
        return {"feedback": feedback, "status": "failed", "rejection_count": 1}
