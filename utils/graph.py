"""
Construction du graphe LangGraph pour l'agent.
"""
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from utils.tools import available_tools
from utils.agent import AgentState, create_agent_node, should_continue

# Charger les variables d'environnement
load_dotenv()


def create_agent_graph():
    """
    Crée et compile le graphe de l'agent.
    
    Returns:
        Graphe compilé prêt à être exécuté
    """
    # Initialiser le LLM avec les tools
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools(available_tools)
    
    # Créer le graphe
    workflow = StateGraph(AgentState)
    
    # Ajouter les nœuds
    agent_node = create_agent_node(llm_with_tools)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(available_tools))
    
    # Définir le point d'entrée
    workflow.set_entry_point("agent")
    
    # Ajouter les edges conditionnelles
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    # Revenir à l'agent après l'exécution des tools
    workflow.add_edge("tools", "agent")
    
    # Compiler le graphe
    return workflow.compile()


def visualize_graph(graph):
    """
    Affiche une visualisation ASCII du graphe.
    
    Args:
        graph: Graphe compilé
    """
    try:
        print("\n=== Structure du Graphe ===")
        print(graph.get_graph().draw_ascii())
    except Exception as e:
        print(f"Impossible d'afficher le graphe : {e}")