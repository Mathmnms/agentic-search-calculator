"""
Tools disponibles pour l'agent.
"""
from langchain_core.tools import tool
from tavily import TavilyClient
import os

@tool
def calculator(expression: str) -> str:
    """
    Calcule une expression mathématique.
    
    Args:
        expression: Expression mathématique à calculer (ex: "2 + 2", "10 * 5")
    
    Returns:
        Le résultat du calcul
    """
    try:
        # Sécurité : n'autoriser que les opérations mathématiques de base
        allowed_chars = set("0123456789+-*/.()")
        if not all(c in allowed_chars or c.isspace() for c in expression):
            return "Erreur : caractères non autorisés dans l'expression"
        
        result = eval(expression)
        return f"Le résultat de {expression} est {result}"
    except Exception as e:
        return f"Erreur de calcul : {str(e)}"


@tool
def web_search(query: str) -> str:
    """
    Recherche des informations sur le web.
    
    Args:
        query: Question ou terme de recherche
    
    Returns:
        Résumé des résultats de recherche
    """
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = tavily_client.search(query, max_results=3)
        
        # Formater les résultats
        results = []
        for result in response.get('results', []):
            results.append(f"- {result['title']}: {result['content'][:200]}...")
        
        return "\n".join(results) if results else "Aucun résultat trouvé"
    except Exception as e:
        return f"Erreur de recherche : {str(e)}"


# Liste des tools disponibles
available_tools = [calculator, web_search]