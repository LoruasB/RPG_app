import streamlit as st
from logic.hp import remover_se_morto
from data.condicoes import CONDICOES

def render_grid(df):
    turno_idx = st.session_state["turno"]

    st.markdown("## ⚔️ Combate")
    
    st.markdown("""
    <style>
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    header_cols = st.columns([3, 2, 4])
    header_cols[0].markdown("**Personagem**")
    header_cols[1].markdown("**Dano/Cura sofrida**")
    header_cols[2].markdown("**Condições**")

    for i, row in df.iterrows():
        hp = st.session_state["hp_editavel"][i]

        if f"mostrar_condicoes_{i}" not in st.session_state:
            st.session_state[f"mostrar_condicoes_{i}"] = False
        if f"dano_cura_{i}" not in st.session_state:
            st.session_state[f"dano_cura_{i}"] = 0

        cols = st.columns([3, 2, 4])

        with cols[0]:
            tipo = row.get("Tipo", "")
            hp_max = row.get("HP", 0) or 0
            status = "💀 Caído" if hp <= 0 else ""
            coracao = "💙" if hp > hp_max else "❤️"

            st.markdown(f"""
            <div class="card {'card-jogador' if tipo == 'Jogador' else 'card-inimigo'}">
                <div style="padding: 8px 0; font-weight: 700; font-size: 18px;">{row['Nome']}</div>
                <div>Tipo: {tipo}</div>
                <div>CA: {row.get('CA', '-')}</div>
                <div>HP: {hp}/{hp_max} {status}</div>
            </div>
            """, unsafe_allow_html=True)

        with cols[1]:
            st.number_input(
                "Valor",
                value=st.session_state[f"dano_cura_{i}"],
                step=1,
                key=f"dano_cura_{i}"
            )
            if st.button("Aplicar", key=f"aplicar_dano_{i}"):
                delta = st.session_state[f"dano_cura_{i}"]
                novo_hp = max(0, hp + delta)
                st.session_state["hp_editavel"][i] = novo_hp
                if novo_hp == 0:
                    remover_se_morto(i)
                st.rerun()

        with cols[2]:
            if st.button("Add condição", key=f"btn_add_cond_{i}"):
                st.session_state[f"mostrar_condicoes_{i}"] = not st.session_state[f"mostrar_condicoes_{i}"]

            if st.session_state[f"mostrar_condicoes_{i}"]:
                st.session_state["condicoes"][i] = st.multiselect(
                    "Condições",
                    list(CONDICOES.keys()),
                    default=st.session_state["condicoes"][i],
                    key=f"multi_cond_{i}"
                )

            if st.session_state["condicoes"][i]:
                cond_text = " ".join([
                    f"{CONDICOES[c]} {c}"
                    for c in st.session_state["condicoes"][i]
                ])
                st.markdown(cond_text)
            else:
                st.write("Sem condições")

        st.markdown("<hr style='margin: 16px;'>", unsafe_allow_html=True)
