"""
Exemples d'utilisation de l'agent.
"""
from utils.graph import create_agent_graph
from langchain_core.messages import HumanMessage


def run_example(query: str):
    """Exécute un exemple et affiche le résultat."""
    print(f"\n{'='*60}")
    print(f"Question: {query}")
    print(f"{'='*60}\n")
    
    graph = create_agent_graph()
    inputs = {"messages": [HumanMessage(content=query)]}
    
    result = graph.invoke(inputs)
    final_message = result["messages"][-1]
    
    print(f"Réponse: {final_message.content}\n")


if __name__ == "__main__":
    # Exemples variés pour démonstration
    examples = [
        # Calcul simple
        "Combien font 234 * 567?",
        
        # Recherche simple
        "Qui est le président de la France en 2024?",
        
        # Combinaison recherche + calcul
        "Quelle est la population de Tokyo et divise-la par 1000000",
        
        # Question complexe
        "Cherche le PIB de l'Allemagne et calcule 10% de ce montant",
    ]
    
    for example in examples:
        run_example(example)
        input("Appuyez sur Entrée pour continuer...")