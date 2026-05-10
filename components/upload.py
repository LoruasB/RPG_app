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
    # CONTROLES DE EXIBIÇÃO
    # =========================
    if "show_personagens" not in st.session_state:
        st.session_state["show_personagens"] = False
    if "show_inimigos" not in st.session_state:
        st.session_state["show_inimigos"] = False
    if "show_adicionar_inimigo" not in st.session_state:
        st.session_state["show_adicionar_inimigo"] = False
    if "inimigos_extra" not in st.session_state:
        st.session_state["inimigos_extra"] = []

    col1, col2, col3 = st.columns(3)
    if col1.button("Ver Personagens", key="btn_ver_personagens"):
        st.session_state["show_personagens"] = not st.session_state["show_personagens"]
    if col2.button("Ver Inimigos", key="btn_ver_inimigos"):
        st.session_state["show_inimigos"] = not st.session_state["show_inimigos"]
    if col3.button("Add Inimigo", key="btn_add_inimigo"):
        st.session_state["show_adicionar_inimigo"] = not st.session_state["show_adicionar_inimigo"]

    if st.session_state["show_personagens"]:
        st.subheader("📋 Personagens")
        st.dataframe(df_personagens, use_container_width=True)

    if st.session_state["show_inimigos"]:
        st.subheader("👾 Inimigos")
        st.dataframe(df_inimigos, use_container_width=True)

    # =========================
    # INIMIGOS EXTRA
    # =========================
    if st.session_state["show_adicionar_inimigo"]:
        st.subheader("➕ Adicionar inimigo extra")
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

        if st.session_state["inimigos_extra"]:
            st.subheader("🧟 Inimigos extras adicionados")
            st.dataframe(
                pd.DataFrame(st.session_state["inimigos_extra"]),
                use_container_width=True
            )

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