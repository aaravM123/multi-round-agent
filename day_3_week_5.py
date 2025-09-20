readme = """
# Multi-Round Task Agent (LangGraph + OpenAI)

This AI agent uses LangGraph to:
- Plan a new task each round using a planner role
- Execute the task using an executor role
- Reflect on the result using a reviewer role
- Repeat the plan → execute → review cycle for multiple rounds

### Example Use Cases:
- Autonomous study planner (e.g., 3-day math review)
- Productivity bot that executes and evaluates daily tasks
- Research assistant that cycles through tasks and improvements
- AI simulation of goal-oriented behavior over time

### Files:
- langgraph_multi_round_agent.ipynb: Full agent logic in Google Colab
- requirements.txt: Python dependencies
- README.md: This file

### Run Instructions:
```bash
pip install -r requirements.txt
# Then open and run the notebook in Google Colab
"""

with open("README.md", "w") as f:
  f.write(readme)
!cat README.md  # to preview

!pip install -q langgraph openai

from getpass import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass("Enter your own OpenAI API Key: ")

state_schema = dict

# Planner Node
def planner_node(state):
  round_num = state.get("round", 1)
  print(f"Planner: Planning task for Day {round_num}...")
  task = f"{round_num} + {round_num}"
  logs = state.get("log", [])
  logs.append(f"Planned task for Day {round_num}")
  return {
      **state,
      "task": task,
      "role": "executor",
      "log": logs
  }

# Role Switch Node
def role_switch_node(state):
  print(f"Switching role to: {state.get('role')}")

# Step 3: Routing function based on role
def route_by_role(state):
  role = state.get("role", "")
  if role == "executor":
    return "executor_node"
  elif role == "reviewer":
    return "reviewer_node"
  elif role == "planner":
    return "planner_node"
  else:
    return "end"

# Step 4: Executor node
def executor_node(state):
  task = state.get("task", "")
  print(f"Executor: Executing task: {task}")
  try:
    result = eval(task)
  except Exception as e:
    result = f"Error: {e}"
  logs = state.get("log", [])
  logs.append(f"Executed task: {task} -> Result: {result}")
  return {**state, "result": result, "role": "reviewer","log": logs}

# Step 5: Review Node
def reviewer_node(state):
  round_num = state.get("round", 1)
  max_rounds = state.get("max_rounnds", 3)

  print(f"Reviewer: Reflecting on Day {round_num}...")
  logs = state.get("log", [])
  logs.append(f"Reviewed task for Day {round_num}")

  if round_num < max_rounds:
    return {**state, "round": round_num + 1, "role": "planner", "log": logs}
  else:
    return {**state, "role": "end", "log": logs}

# Step 6: End Node
def end_node(state):
  print("Finished")
  print(state)
  return state

builder = StateGraph(state_schema)

# Add Nodes
builder.add_node("planner_node", planner_node)
builder.add_node("role_switch", role_switch_node)
builder.add_node("executor_node", executor_node)
builder.add_node("reviewer_node", reviewer_node)
builder.add_node("end", end_node)

# Entry Point
builder.set_entry_point("planner_node")

# Add Edges
builder.add_edge("planner_node", "role_switch")
builder.add_conditional_edges("role_switch", route_by_role)
builder.add_edge("executor_node", "role_switch")
builder.add_edge("reviewer_node", "end")

# Compile and Run
graph = builder.compile()

state = {"role": "planner", "round": 1, "max_rounds": 3}

while state.get("role") != "end":
  state = graph.invoke(state)

## ✅ `requirements.txt` (LangGraph + OpenAI)

with open("requirements.txt", "w") as f:
    f.write("openai>=1.0.0\n")
    f.write("langgraph>=0.0.35\n")
    f.write("langchain>=0.1.0\n")

!cat requirements.txt

from google.colab import files
files.download("requirements.txt")
