import requests
import streamlit as st

# ==========================================
# --- DICTIONNAIRES DES MODÈLES ---
# ==========================================

# 1. Modèles OpenRouter (Cloud)
MODELES_OPENROUTER = {
    "1. Modèles Gratuits": [
        "openrouter/free",
        "baidu/ernie-5.5-flash-preview:free",
        "deepseek/deepseek-v4.1-flash",
        "nvidia/nemotron-3.5-lightning:free",
        "google/gemma-4-31b-it",
        "cohere/north-mini-code:free",
        "qwen/qwen-2.5-72b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
    ],
    "2. Modèles Très Économiques": [
        "meta-llama/llama-3.3-70b-instruct:free",
        "qwen/qwen3.6-plus",
        "qwen/qwen3-coder-30b-a3b-instruct",
        "google/gemini-2.0-flash-001",
        "openai/gpt-4o-mini",
    ],
    "3. Modèles Haute Performance": [
        "anthropic/claude-sonnet-5.5",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-opus-5.5",
        "google/gemini-2.5-pro",
    ]
}

# 2. Modèles Ollama (Local) - Nettoyés et organisés
MODELES_OLLAMA = {
    "1. Cybersécurité & Pentesting": [
        "monotykamary/whiterabbitneo-v1.5a:7b",
        "hf.co/QuantFactory/Lily-Cybersecurity-7B-v0.2-GGUF:Q4_K_M",
        "jimscard/blackhat-hacker:latest",
        "jimscard/whiterabbit-neo:13b",
        "llama3.2:3b-pentagi",
        "qwen2.5-coder:7b-pentagi",
        "qwen2.5-coder:7b-pentagi-v2",
    ],
    "2. Code & Raisonnement": [
        "huihui_ai/deepseek-r1-abliterated:7b",
        "deepseek-r1:8b",
        "huihui_ai/qwen3.5-abliterated:9b",
        "qwen3.5:4b",
        "qwen35-fast:latest",
        "qwen2.5-coder:7b",
    ],
    "3. Généralistes & Légers": [
        "llama3.2:latest",
        "llama3.2:1b",
        "llama3.2:3b",
        "llama3.1:8b",
        "gemma3:4b",
        "dolphin-mistral:7b",
        "openhermes:7b-v2.5",
    ]
}

# ==========================================
# --- CONFIGURATION DU DESIGN (CSS) ---
# ==========================================
st.markdown("""
<style>
    /* Fond rose pour la barre latérale */
    section[data-testid="stSidebar"] {
        background-color: #ffe4e1 !important;
        border-right: 2px solid #ffb6c1;
    }
    /* Accentuation de la zone de texte */
    .stTextArea textarea {
        border: 3px solid #ff69b4 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        box-shadow: 0px 4px 10px rgba(255, 105, 180, 0.2) !important;
        font-size: 16px !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #ff1493 !important;
        box-shadow: 0px 4px 15px rgba(255, 20, 147, 0.4) !important;
    }
    /* Style général des boutons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    /* Style spécifique pour les boutons icônes */
    .icon-btn button {
        background-color: transparent !important;
        color: #ff1493 !important;
        border: 2px solid #ffb6c1 !important;
        font-size: 20px !important;
        padding: 5px 10px !important;
    }
    .icon-btn button:hover {
        background-color: #ffe4e1 !important;
        border-color: #ff69b4 !important;
    }
    /* Style pour la zone de réponse (texte en noir) */
    .response-box {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff69b4;
        color: #000000 !important; /* Force le texte en noir */
        font-size: 16px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- TITRE DE L'APPLICATION ---
st.title("PAKO_IA")

# --- Initialisation de la mémoire ---
if "last_response" not in st.session_state:
    st.session_state.last_response = ""
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""
if "texte_a_envoyer" not in st.session_state:
    st.session_state.texte_a_envoyer = ""


# --- FONCTION DE RAPPEL (CALLBACK) ---
def soumettre_et_vider():
    st.session_state.texte_a_envoyer = st.session_state.user_prompt
    st.session_state.user_prompt = ""
    st.session_state.show_uploader = False


# ==========================================
# --- BARRE LATÉRALE : FOURNISSEURS & MODÈLES ---
# ==========================================
fournisseur = st.sidebar.radio("Fournisseur d'IA", ["OpenRouter (Cloud)", "Ollama (Local)"])

if fournisseur == "OpenRouter (Cloud)":
    api_key = st.sidebar.text_input("Clé API OpenRouter", type="password")

    # Menus pour OpenRouter
    categorie_or = st.sidebar.selectbox(
        "Catégorie (Cloud)",
        list(MODELES_OPENROUTER.keys())
    )
    model = st.sidebar.selectbox(
        "Choisir un modèle (Cloud)",
        MODELES_OPENROUTER[categorie_or]
    )
else:
    api_key = "ollama"

    # Menus pour Ollama
    categorie_ollama = st.sidebar.selectbox(
        "Catégorie (Local)",
        list(MODELES_OLLAMA.keys())
    )
    model = st.sidebar.selectbox(
        "Choisir un modèle (Local)",
        MODELES_OLLAMA[categorie_ollama]
    )

# ==========================================
# --- ZONE DE SAISIE ET BARRE D'OUTILS ---
# ==========================================
prompt = st.text_area("Votre message :", height=120, key="user_prompt")

if st.session_state.show_uploader:
    uploaded_file = st.file_uploader("Ajouter un fichier (TXT)", label_visibility="collapsed")
else:
    uploaded_file = None

# Création des colonnes pour la barre d'outils
col_plus, col_mic, col_paperclip, col_send = st.columns([1, 1, 1, 6])

with col_plus:
    st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
    if st.button("➕", help="Ajouter un fichier"):
        st.session_state.show_uploader = not st.session_state.show_uploader
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_mic:
    st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
    audio_value = st.audio_input("🎤", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col_paperclip:
    st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
    export_text = st.session_state.last_response if st.session_state.last_response else "Aucune conversation."
    st.download_button(
        label="📎",
        data=export_text,
        file_name="conversation_pako_ia.txt",
        mime="text/plain",
        help="Exporter la dernière réponse"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_send:
    envoye = st.button("Envoyer", use_container_width=True, type="primary", on_click=soumettre_et_vider)

# ==========================================
# --- TRAITEMENT DE L'ENVOI ---
# ==========================================
if st.session_state.texte_a_envoyer:
    final_prompt = st.session_state.texte_a_envoyer

    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            file_content = uploaded_file.read().decode("utf-8")
            final_prompt += f"\n\n[Contenu du fichier joint :]\n{file_content}"
        else:
            final_prompt += f"\n\n[Un fichier '{uploaded_file.name}' a été joint.]"

    if audio_value is not None:
        final_prompt += "\n\n[L'utilisateur a dicté un message audio.]"

    # Configuration de la requête
    if fournisseur == "OpenRouter (Cloud)":
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "PAKO_IA",
            "Content-Type": "application/json",
        }
    else:
        url = "http://localhost:11434/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

    try:
        with st.spinner("Génération en cours..."):
            response = requests.post(
                url=url, headers=headers,
                json={"model": model.strip(), "messages": [{"role": "user", "content": final_prompt}]},
                timeout=120,  # Augmenté à 120s pour les modèles locaux qui peuvent être lents
            )

        if response.status_code == 200:
            try:
                data = response.json()
                st.session_state.last_response = data["choices"][0]["message"]["content"]

                st.session_state.texte_a_envoyer = ""
                st.rerun()

            except requests.exceptions.JSONDecodeError:
                st.error(f"Réponse inattendue du serveur (non-JSON) : {response.text[:500]}")
                st.session_state.texte_a_envoyer = ""
        else:
            st.error(f"Erreur HTTP {response.status_code} : {response.text}")
            st.session_state.texte_a_envoyer = ""

    except requests.exceptions.ConnectionError:
        st.error("Impossible de joindre le serveur. Vérifiez la connexion ou Ollama.")
        st.session_state.texte_a_envoyer = ""
    except Exception as e:
        st.error(f"Erreur : {e}")
        st.session_state.texte_a_envoyer = ""

# ==========================================
# --- AFFICHAGE DE LA RÉPONSE ---
# ==========================================
if st.session_state.last_response:
    st.markdown("### Réponse de PAKO_IA :")
    st.markdown(
        f'<div class="response-box">{st.session_state.last_response}</div>',
        unsafe_allow_html=True
    )
    
