"""
Interface Streamlit pour l'agent LangGraph - Recherche & Calcul.
"""
import streamlit as st
from dotenv import load_dotenv
from utils.graph import create_agent_graph
from langchain_core.messages import HumanMessage
import os

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Agent ReAct - Recherche & Calcul",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .tool-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        margin: 0.3rem;
        background-color: #e3f2fd;
        color: #1976d2;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialise l'état de la session."""
    if 'graph' not in st.session_state:
        st.session_state.graph = create_agent_graph()
    if 'history' not in st.session_state:
        st.session_state.history = []


def display_header():
    """Affiche l'en-tête de l'application."""
    st.markdown('<h1 class="main-header">🤖 Agent ReAct - Recherche & Calcul</h1>', 
                unsafe_allow_html=True)
    st.markdown("### Architecture LangGraph avec pattern ReAct")
    st.markdown("---")


def display_sidebar():
    """Affiche la barre latérale."""
    with st.sidebar:
        st.header("📊 À propos")
        st.markdown("""
        Cet agent utilise le **pattern ReAct** (Reasoning + Acting) 
        avec **LangGraph** pour répondre à vos questions.
        
        ### 🛠️ Tools disponibles:
        
        <div class="tool-badge">🧮 Calculatrice</div>
        
        - Calculs mathématiques
        - Opérations arithmétiques
        
        <div class="tool-badge">🔍 Recherche Web</div>
        
        - Recherche d'informations
        - Actualités et faits
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Exemples de questions
        st.header("💡 Exemples de questions")
        examples = [
            "Combien font 234 * 567 ?",
            "Qui a gagné la coupe du monde 2022 ?",
            "Calcule 15% de 2000",
            "Quelle est la population de la France ?",
            "Combien font 156 * 234 + 1000 ?",
        ]
        
        for example in examples:
            if st.button(example, key=example, use_container_width=True):
                st.session_state.current_query = example
        
        st.markdown("---")
        
        # Statistiques
        if st.session_state.history:
            st.header("📊 Statistiques")
            st.metric("Requêtes traitées", len(st.session_state.history))


def display_main_interface():
    """Affiche l'interface principale."""
    
    # Vérifier les clés API
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OPENAI_API_KEY non trouvée. Veuillez configurer votre fichier .env")
        return
    
    # Zone de saisie
    col1, col2 = st.columns([5, 1])
    
    with col1:
        query = st.text_input(
            "💬 Posez votre question :",
            value=st.session_state.get('current_query', ''),
            placeholder="Ex: Combien font 123 * 456 ? ou Qui a gagné le mondial 2022 ?",
            key="query_input"
        )
    
    with col2:
        st.write("")  # Espaceur
        st.write("")  # Espaceur
        submit = st.button("🚀 Analyser", type="primary", use_container_width=True)
    
    # Traiter la requête
    if submit and query:
        with st.spinner("🔄 L'agent réfléchit..."):
            try:
                # Préparer l'input
                inputs = {"messages": [HumanMessage(content=query)]}
                
                # Exécuter l'agent
                result = st.session_state.graph.invoke(inputs)
                
                # Récupérer la réponse finale
                final_message = result["messages"][-1]
                response = final_message.content
                
                # Ajouter à l'historique
                st.session_state.history.append({
                    "query": query,
                    "response": response
                })
                
                # Afficher le résultat
                st.markdown("---")
                st.markdown("### 💡 Réponse :")
                st.markdown(response)
                
                # Réinitialiser la requête
                if 'current_query' in st.session_state:
                    del st.session_state.current_query
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
    
    # Afficher l'historique
    if st.session_state.history:
        st.markdown("---")
        st.header("📜 Historique des requêtes")
        
        # Afficher les 5 dernières requêtes (inversé)
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"🔹 {item['query']}", expanded=(i==0)):
                st.markdown(item['response'])
        
        # Bouton pour effacer l'historique
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.history = []
            st.rerun()


def main():
    """Fonction principale."""
    initialize_session_state()
    display_header()
    display_sidebar()
    display_main_interface()


if __name__ == "__main__":
    main()