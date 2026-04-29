import streamlit as st

def aplicar_css(cor_fundo, cor_jogador, cor_jogador_turno, cor_inimigo, cor_inimigo_turno):
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {cor_fundo}; }}

    .card {{
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
    }}

    .card-jogador {{ background-color: {cor_jogador}; }}
    
    .card-jogador-turno {{
        background-color: {cor_jogador_turno};
        border: 2px solid white;
    }}

    .card-inimigo {{ background-color: {cor_inimigo}; }}
    
    .card-inimigo-turno {{
        background-color: {cor_inimigo_turno};
        border: 2px solid white;
    }}

    div.stButton > button {{
        font-size: 8px;
        padding: 2px;
        border-radius: 20px;
        min-width: 25px;
    }}

    button[kind="secondary"] {{
        font-size: 14px;
        padding: 6px 10px;
    }}

    </style>
    """, unsafe_allow_html=True)