import streamlit as st

def remover_se_morto(index):
    df = st.session_state["combate"]
    hp_lista = st.session_state["hp_editavel"]

    if df.loc[index, "Tipo"] == "Inimigo" and hp_lista[index] <= 0:
        df = df.drop(index).reset_index(drop=True)
        hp_lista.pop(index)

        if st.session_state["turno"] >= len(df):
            st.session_state["turno"] = 0

        st.session_state["combate"] = df
        st.session_state["hp_editavel"] = hp_lista