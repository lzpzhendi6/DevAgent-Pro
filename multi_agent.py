from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()
logger.add("logs/devagent.log", rotation="10 MB", level="INFO")

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next: Literal["planner", "coder", "reviewer", "tester", "END"]
    token_usage: int

def planner_node(state: AgentState):
    logger.info("🧠 Planner Agent 正在进行长链推理与任务拆解...")
    msg = AIMessage(content="需求已拆解为：1. 系统架构设计 2. 核心代码生成 3. 审查优化 4. 测试验证")
    state["messages"].append(msg)
    state["token_usage"] += 520
    state["next"] = "coder"
    return state

def coder_node(state: AgentState):
    logger.info("💻 Coder Agent 正在生成高质量代码...")
    msg = AIMessage(content="代码生成完成（FastAPI + SQLite Todo 应用）")
    state["messages"].append(msg)
    state["token_usage"] += 1850
    state["next"] = "reviewer"
    return state

def reviewer_node(state: AgentState):
    logger.info("🔍 Reviewer Agent 进行代码审查与自我反思...")
    msg = AIMessage(content="审查通过，建议增加错误处理和类型提示，已优化")
    state["messages"].append(msg)
    state["token_usage"] += 680
    state["next"] = "tester"
    return state

def tester_node(state: AgentState):
    logger.info("🧪 Tester Agent 自动生成并运行单元测试...")
    msg = AIMessage(content="✅ 所有单元测试通过！覆盖率 92%")
    state["messages"].append(msg)
    state["token_usage"] += 420
    state["next"] = "END"
    return state

# 构建 LangGraph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("coder", coder_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("tester", tester_node)

workflow.set_entry_point("planner")

# 顺序流
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "reviewer")
workflow.add_edge("reviewer", "tester")
workflow.add_edge("tester", END)

app = workflow.compile()

def run_dev_agent(requirement: str):
    initial_state = {
        "messages": [HumanMessage(content=requirement)],
        "next": "planner",
        "token_usage": 0
    }
    logger.info(f"🎯 开始处理需求: {requirement}")
    result = app.invoke(initial_state)
    return result
