import streamlit as st
import pandas as pd
from logic.iniciativa import calcular_iniciativa

def render_upload():
    uploaded_file = st.file_uploader("Envie o Excel", type=["xlsx"])

    if not uploaded_file:
        return

    try:
        excel = pd.ExcelFile(uploaded_file)

        df_personagens = pd.read_excel(excel, sheet_name="Personagens")
        df_inimigos = pd.read_excel(excel, sheet_name="Inimigos")

        df_personagens.columns = df_personagens.columns.str.strip()
        df_inimigos.columns = df_inimigos.columns.str.strip()

    except Exception as e:
        st.error(f"❌ Erro ao ler arquivo: {e}")
        st.stop()

    # =========================
    # EXIBIÇÃO
    # =========================
    st.subheader("📋 Personagens")
    st.dataframe(df_personagens, use_container_width=True)

    st.subheader("👾 Inimigos")
    st.dataframe(df_inimigos, use_container_width=True)

    # =========================
    # INIMIGOS EXTRA
    # =========================
    if "inimigos_extra" not in st.session_state:
        st.session_state["inimigos_extra"] = []

    with st.form("form_inimigo"):
        nome = st.text_input("Nome inimigo")
        ini = st.number_input("Iniciativa", step=1)
        hp = st.number_input("HP", step=1)
        ca = st.number_input("CA", step=1)
        dex = st.number_input("DEX", step=1)

        if st.form_submit_button("Adicionar") and nome:
            st.session_state["inimigos_extra"].append({
                "Nome": nome,
                "Iniciativa": ini,
                "HP": hp,
                "CA": ca,
                "DEX": dex
            })

    # =========================
    # ROLAR INICIATIVA
    # =========================
    if st.button("🎲 Rolar iniciativa"):

        df_final = calcular_iniciativa(
            df_personagens,
            df_inimigos,
            st.session_state["inimigos_extra"]
        )

        st.subheader("🎲 Resultados de Iniciativa")
        st.dataframe(
            df_final.drop(columns=["DEX", "IniBase"]),
            use_container_width=True
        )

        # =========================
        # ESTADO
        # =========================
        st.session_state["combate"] = df_final
        st.session_state["turno"] = 0
        st.session_state["rodada"] = 1
        st.session_state["hp_editavel"] = df_final["HP"].fillna(0).tolist()
        st.session_state["condicoes"] = [[] for _ in range(len(df_final))]