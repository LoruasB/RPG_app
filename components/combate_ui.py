import streamlit as st
from logic.hp import remover_se_morto

def render_turno(df):
    turno_idx = st.session_state["turno"]

    st.markdown(f"## 🔁 Rodada {st.session_state['rodada']}")
    st.markdown("## 🎯 Turno Atual")

    row = df.iloc[turno_idx]
    hp_atual = st.session_state["hp_editavel"][turno_idx]
    hp_max = row["HP"] if row["HP"] else 1

    col1, col2, col3 = st.columns([1,3,1])

    with col1:
        if st.button("◀", key="prev_turn"):
            if turno_idx == 0:
                st.session_state["turno"] = len(df) - 1
                if st.session_state["rodada"] > 1:
                    st.session_state["rodada"] -= 1
            else:
                st.session_state["turno"] -= 1
            st.rerun()

    with col2:
        st.markdown(f"<h3 style='text-align:center; margin: 0;'> {row['Nome']} </h3>", unsafe_allow_html=True)

    with col3:
        if st.button("▶", key="next_turn"):
            if turno_idx == len(df) - 1:
                st.session_state["turno"] = 0
                st.session_state["rodada"] += 1
            else:
                st.session_state["turno"] += 1
            st.rerun()

    st.markdown("---")