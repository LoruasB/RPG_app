import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🎨 Cores")

        cor_fundo = st.color_picker("", "#BCD5FF", label_visibility="collapsed")

        st.markdown("**Jogadores**")
        cor_jogador = st.color_picker("Normal", "#41A7F0", key="cj1")
        cor_jogador_turno = st.color_picker("Turno", "#1D4864", key="cj2")

        st.markdown("**Inimigos**")
        cor_inimigo = st.color_picker("Normal", "#F8432F", key="ci1")
        cor_inimigo_turno = st.color_picker("Turno", "#7D241A", key="ci2")

    return cor_fundo, cor_jogador, cor_jogador_turno, cor_inimigo, cor_inimigo_turno