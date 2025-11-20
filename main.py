"""
Point d'entrée principal pour l'agent LangGraph.
"""
from langchain_core.messages import HumanMessage
from utils.graph import create_agent_graph, visualize_graph


def run_agent(query: str):
    """
    Exécute l'agent avec une requête utilisateur.
    
    Args:
        query: Question ou instruction pour l'agent
    """
    print(f"\n{'='*60}")
    print(f"🤖 Question: {query}")
    print(f"{'='*60}\n")
    
    # Créer le graphe
    graph = create_agent_graph()
    
    # Préparer l'input
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # Exécuter l'agent
    print("🔄 L'agent réfléchit...\n")
    
    for output in graph.stream(inputs):
        for key, value in output.items():
            print(f"📍 Étape: {key}")
            if "messages" in value:
                last_message = value["messages"][-1]
                
                # Afficher les appels de tools
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"  🔧 Appel du tool: {tool_call['name']}")
                        print(f"  📥 Arguments: {tool_call['args']}")
                
                # Afficher le contenu du message
                if hasattr(last_message, 'content') and last_message.content:
                    print(f"  💬 Réponse: {last_message.content}")
            
            print()
    
    # Récupérer la réponse finale
    final_output = list(graph.stream(inputs))[-1]
    final_message = final_output[list(final_output.keys())[0]]["messages"][-1]
    
    print(f"{'='*60}")
    print(f"✅ RÉPONSE FINALE:")
    print(f"{'='*60}")
    print(final_message.content)
    print(f"{'='*60}\n")


def main():
    """
    Fonction principale avec des exemples de requêtes.
    """
    print("\n" + "="*60)
    print("🚀 AGENT LANGGRAPH - RECHERCHE & CALCUL")
    print("="*60)
    
    # Afficher la structure du graphe
    graph = create_agent_graph()
    visualize_graph(graph)
    
    # Exemples de requêtes
    examples = [
        "Quelle est la population de la France et multiplie ce nombre par 2?",
        "Calcule 156 * 234 + 1000",
        "Qui a gagné la coupe du monde de football 2022?",
    ]
    
    print("\n" + "="*60)
    print("📋 EXEMPLES DE REQUÊTES")
    print("="*60)
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "="*60)
    
    # Demander à l'utilisateur
    choice = input("\nChoisissez un exemple (1-3) ou tapez votre propre question: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(examples):
        query = examples[int(choice) - 1]
    else:
        query = choice
    
    if query:
        run_agent(query)
    else:
        print("❌ Aucune question fournie.")


if __name__ == "__main__":
    main()