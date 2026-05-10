import streamlit as st

def aplicar_css(cor_fundo, cor_jogador, cor_jogador_turno, cor_inimigo, cor_inimigo_turno):
    st.markdown(f"""
    <style>
    .stApp {{ 
        background-color: {cor_fundo};
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: {cor_fundo};
    }}

    [data-testid="stMainBlockContainer"] {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 3rem 20px 0 20px;
    }}

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

    button[key^="up_"], button[key^="down_"] {{
        font-size: 10px;
        padding: 2px 4px;
    }}

    .card {{
        position: relative;
    }}

    .card-botoes {{
        position: absolute;
        top: 6px;
        left: 6px;
        display: flex;
        gap: 4px;
    }}

    .card-botoes button {{
        background: transparent;
        border: none;
        box-shadow: none;
        font-size: 12px;
        padding: 2px;
        cursor: pointer;
    }}

    .card-botoes button:hover {{
        transform: scale(1.2);
    }}

    </style>
    """, unsafe_allow_html=True)