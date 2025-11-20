# Architecture de l'Agent

## Diagramme du Graphe LangGraph
```
┌─────────────────────────────────────────────────┐
│                    START                        │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │                       │
         │    AGENT NODE         │
         │  (LLM Reasoning)      │
         │                       │
         │  - Analyse la query   │
         │  - Décide du tool     │
         │  - Génère réponse     │
         │                       │
         └───────────┬───────────┘
                     │
            ┌────────┴────────┐
            │                 │
      Tool calls?        Pas de tool
            │                 │
            ▼                 ▼
    ┌──────────────┐      ┌──────┐
    │  TOOLS NODE  │      │ END  │
    │              │      └──────┘
    │ - calculator │
    │ - web_search │
    │              │
    └──────┬───────┘
           │
           │ (Retour avec résultat)
           │
           └──────► (Retour à AGENT NODE)
```

## Flow d'Exécution

### Exemple : "Quelle est la population de la France multiplié par 2?"

1. **User Input** → Agent Node
2. **Agent Node** → Décide d'utiliser `web_search`
3. **Tools Node** → Exécute `web_search("population France")`
4. **Tools Node** → Retour vers Agent Node avec résultat
5. **Agent Node** → Décide d'utiliser `calculator`
6. **Tools Node** → Exécute `calculator("67000000 * 2")`
7. **Tools Node** → Retour vers Agent Node
8. **Agent Node** → Génère réponse finale
9. **END** → Retourne la réponse à l'utilisateur

## Composants Techniques

### State Management
```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```

### Decision Logic
```python
def should_continue(state: AgentState) -> str:
    if has_tool_calls:
        return "continue"  # → Tools Node
    else:
        return "end"       # → END
```

### Tools
- **calculator**: Évalue des expressions mathématiques
- **web_search**: Recherche via l'API Tavily