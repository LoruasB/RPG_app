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
        st.markdown(f"<h3 style='text-align:center;'> {row['Nome']}</h3>", unsafe_allow_html=True)

    with col3:
        if st.button("▶", key="next_turn"):
            if turno_idx == len(df) - 1:
                st.session_state["turno"] = 0
                st.session_state["rodada"] += 1
            else:
                st.session_state["turno"] += 1
            st.rerun()

    if row["Tipo"] == "Inimigo":
        col_1, col_2, col_3, col_4, col_5 = st.columns([1,1,2,1,1])

        with col_1:
            if st.button("➖", key="hp_m1"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual - 1)
                remover_se_morto(turno_idx)
                st.rerun()

        with col_2:
            if st.button("-5", key="hp_mi5"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual - 5)
                remover_se_morto(turno_idx)
                st.rerun()

        with col_3:
            proporcao = hp_atual / hp_max if hp_max > 0 else 0
            barra = min(proporcao, 1)
            st.progress(barra)

            proporcao_base = min(proporcao, 1)

            if proporcao_base > 0.6:
                cor_texto = "🟢"
            elif proporcao_base > 0.3:
                cor_texto = "🟡"
            else:
                cor_texto = "🔴"

            excesso = hp_atual - hp_max

            if excesso > 0:
                st.markdown(f"""
                <div style='text-align:center;'>
                    {cor_texto} {hp_atual}/{hp_max}<br>
                    <span style='color:#4FC3F7;'>🔵 +{excesso}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center;'>{cor_texto} {hp_atual}/{hp_max}</div>", unsafe_allow_html=True)

        with col_4:
            if st.button("+5", key="hp_p5"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual + 5)
                remover_se_morto(turno_idx)
                st.rerun()

        with col_5:
            if st.button("➕", key="hp_p1"):
                st.session_state["hp_editavel"][turno_idx] += 1
                st.rerun()

    st.markdown("---")