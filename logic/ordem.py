import streamlit as st

def mover_posicao(index, direcao):
    df = st.session_state["combate"]
    hp = st.session_state["hp_editavel"]
    cond = st.session_state["condicoes"]

    novo_index = index + direcao

    if novo_index < 0 or novo_index >= len(df):
        return

    # swap dataframe
    df.iloc[[index, novo_index]] = df.iloc[[novo_index, index]].values

    # swap listas auxiliares
    hp[index], hp[novo_index] = hp[novo_index], hp[index]
    cond[index], cond[novo_index] = cond[novo_index], cond[index]

    # ajustar turno
    if st.session_state["turno"] == index:
        st.session_state["turno"] = novo_index
    elif st.session_state["turno"] == novo_index:
        st.session_state["turno"] = index

    st.session_state["combate"] = df
    st.session_state["hp_editavel"] = hp
    st.session_state["condicoes"] = cond