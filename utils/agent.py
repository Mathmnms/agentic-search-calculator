"""
Configuration de l'agent et du state.
"""
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    État de l'agent qui stocke l'historique des messages.
    """
    messages: Annotated[list, add_messages]


def create_agent_node(llm_with_tools):
    """
    Crée le nœud agent qui appelle le LLM.
    
    Args:
        llm_with_tools: LLM configuré avec les tools
    
    Returns:
        Fonction du nœud agent
    """
    def agent_node(state: AgentState):
        """Nœud qui fait raisonner l'agent."""
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    return agent_node


def should_continue(state: AgentState) -> str:
    """
    Décide si l'agent doit continuer ou terminer.
    
    Args:
        state: État actuel de l'agent
    
    Returns:
        "continue" si l'agent veut appeler un tool, "end" sinon
    """
    last_message = state["messages"][-1]
    
    # Si le message contient des tool_calls, continuer
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    
    # Sinon, terminer
    return "end"