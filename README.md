# 🤖 Agent LangGraph - Recherche & Calcul

Agent intelligent utilisant LangGraph pour effectuer des recherches web et des calculs mathématiques.

## 📋 Description

Cet agent utilise le pattern **ReAct** (Reasoning + Acting) pour :
- 🔍 Rechercher des informations sur le web via Tavily
- 🧮 Effectuer des calculs mathématiques
- 💡 Combiner plusieurs outils pour répondre à des questions complexes

## 🏗️ Architecture
```
┌─────────────┐
│    Input    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Agent    │ ◄──┐
│  (Reasoning)│    │
└──────┬──────┘    │
       │           │
       ▼           │
┌─────────────┐    │
│   Tools     │────┘
│ - Search    │
│ - Calculator│
└─────────────┘
       │
       ▼
┌─────────────┐
│   Answer    │
└─────────────┘
```

### Composants

- **Agent Node** : Raisonnement du LLM (GPT-4o-mini)
- **Tools Node** : Exécution des outils (calculatrice, recherche web)
- **State** : Gestion de l'historique des messages

## 🚀 Installation

### Prérequis

- Python 3.9+
- Clés API :
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Tavily](https://tavily.com/)

### Étapes

1. Cloner le repository :
```bash
git clone https://github.com/Mathmnms/agentic-search-calculator.git
cd agentic-search-calculator
```

2. Créer un environnement virtuel :
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip3 install -r requirements.txt
```

4. Configurer les clés API :
```bash
cp .env.example .env
# Éditez .env et ajoutez vos clés
```

## 💻 Utilisation

### Mode Interactif
```bash
python3 main.py
```

### Exemples de questions

- "Quelle est la population de la France et multiplie ce nombre par 2?"
- "Calcule 156 * 234 + 1000"
- "Qui a gagné la coupe du monde de football 2022?"

## 📁 Structure du Projet
```
.
├── main.py                 # Point d'entrée
├── utils/
│   ├── __init__.py
│   ├── tools.py           # Définition des outils
│   ├── agent.py           # Configuration de l'agent
│   └── graph.py           # Construction du graphe LangGraph
├── requirements.txt        # Dépendances Python
├── .env                   # Variables d'environnement (non versionné)
├── .gitignore
└── README.md
```

## 🛠️ Technologies

- **LangChain** : Framework pour applications LLM
- **LangGraph** : Construction de workflows à base de graphes
- **OpenAI GPT-4o-mini** : Modèle de langage
- **Tavily** : API de recherche web

## 📊 Fonctionnalités

- ✅ Recherche web en temps réel
- ✅ Calculs mathématiques sécurisés
- ✅ Raisonnement multi-étapes (ReAct)
- ✅ Gestion de l'état conversationnel
- ✅ Visualisation du graphe d'exécution

## 🔐 Sécurité

- Les clés API sont stockées dans `.env` (non versionné)
- La fonction `eval()` du calculateur n'accepte que des caractères mathématiques

## 📚 Références

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

## 👨‍💻 Auteur

Mathis Meimoun - Projet final MSc Albert - Agentic Systems

## 📄 Licence

Ce projet est créé à des fins éducatives.
