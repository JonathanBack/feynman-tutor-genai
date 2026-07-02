import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# =========================================================
# CONFIGURAÇÃO AMBIENTAL E SESSÃO
# =========================================================

# Isso garante que o Python ache o arquivo .env na mesma pasta do script
base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    print("ERRO: A variável NVIDIA_API_KEY não foi carregada. Verifique o arquivo .env!")

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = NVIDIA_API_KEY
)

# Persona do chatbot (FeynmanTutor)
SYSTEM_PROMPT = """
Você é o FeynmanTutor, um assistente educacional baseado no Método Feynman de aprendizagem. 
Seu objetivo NÃO é dar respostas prontas, mas ajudar o usuário a dominar um assunto avaliando a explicação dele.

Siga estritamente este fluxo:
1. No primeiro contato, cumprimente o usuário com entusiasmo e pergunte qual conceito ou assunto ele deseja aprender hoje.
2. Assim que o usuário disser o tema, peça para ele explicar esse conceito com as próprias palavras, da forma mais simples possível (como se estivesse explicando para uma criança de 10 anos).
3. Quando o usuário explicar, analise a resposta dele buscando:
   - Jargões excessivos ou termos técnicos complexos sem explicação.
   - Lacunas na lógica ou pontos cegos no entendimento.
4. Dê o feedback de forma extremamente amigável:
   - Elogie o que foi bem explicado.
   - Aponte as lacunas de forma socrática, fazendo perguntas que o induzam a pensar.
   - Peça para ele simplificar as partes difíceis.
   - Não se alongue demais nas correções e sugestões, mantenha elas diretas e simples.
5. Repita o processo até que o conceito esteja perfeitamente claro e simples. Nunca entregue o resumo pronto logo de início.
"""

# =========================================================
# STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="FeynmanTutor AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 FeynmanTutor AI")
st.caption("Domine conceitos complexos explicando-os de forma simples.")

# =========================================================
# SIDEBAR 
# =========================================================
with st.sidebar:
    st.header("Sobre")
    st.markdown("""
    Assistente educacional baseado no **Método Feynman**.
                
    Como funciona:
    1. Escolha um assunto difícil.
    2. Explique para o Tutor.
    3. Ele avaliará lacunas e jargões.
    4. Refine até dominar!
    """)

    st.markdown("---")

    if st.button("Limpar conversa"):
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Olá! Sou o FeynmanTutor. Qual conceito ou assunto você gostaria de dominar hoje?"
            }
        ]
        st.rerun()

# =========================================================
# HISTÓRICO
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Olá! Sou o FeynmanTutor. Qual conceito ou assunto você gostaria de dominar hoje?"
        }
    ]

# Exibe histórico na tela
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# INPUT & PROCESSAMENTO
# =========================================================
user_question = st.chat_input("Digite sua resposta ou conceito aqui...")

if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.chat_history:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                stream = client.chat.completions.create(
                    model="mistralai/ministral-14b-instruct-2512",
                    messages=api_messages,
                    temperature=0.15,
                    top_p=1.00,
                    max_tokens=2048,
                    stream=True,
                )

                answer_placeholder = st.empty()
                full_answer = ""

                for chunk in stream:
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if delta.content:
                            full_answer += delta.content
                            answer_placeholder.markdown(full_answer + "▌")

                answer_placeholder.markdown(full_answer)

                st.session_state.chat_history.append({"role": "assistant", "content": full_answer})
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")
