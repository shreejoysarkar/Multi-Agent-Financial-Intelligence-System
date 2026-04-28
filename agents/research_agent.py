import os
import sys


from langchain_ollama import Ollama


# Ensure the root directory is in the path so we can import Toools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Toools.research_tool import *
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

def research_agent(llm):
    """
    Creates a LangGraph research agent equipped with the fetch_local_data and normalize_data tools.
    
    Args:
        llm: The language model instance (rom langchain_ollama).
        
    Returns:
        A compiled LangGraph ReAct agent.
    """
    tools = [fetch_local_data]
    
    system_prompt = (
        "You are a specialized Financial Research Agent. "
        "Your task is to fetch and analyze raw financial data "
        "(such as 'bank_transactions', 'invoices', or 'erp') using the provided tools. "
        "When asked about data, always use the fetch_local_data tool to retrieve it."
    )
    
    system_message = SystemMessage(content=system_prompt)
    
    agent_executor = create_react_agent(
        llm, 
        tools=tools, 
        prompt=system_message
    )
    
    return agent_executor
