
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
