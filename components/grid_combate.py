import streamlit as st
from logic.hp import remover_se_morto
from logic.ordem import mover_posicao
from data.condicoes import CONDICOES

def render_grid(df):
    turno_idx = st.session_state["turno"]

    st.markdown("## ⚔️ Combate")

    num_colunas = 4
    linhas = [df[i:i+num_colunas] for i in range(0, len(df), num_colunas)]

    for linha in linhas:
        cols = st.columns(num_colunas)

        for idx_col, (_, row) in enumerate(linha.iterrows()):
            i = row.name
            hp = st.session_state["hp_editavel"][i]

            with cols[idx_col]:

                # =========================
                # CONTROLE DE VISIBILIDADE
                # =========================
                if f"mostrar_{i}" not in st.session_state:
                    st.session_state[f"mostrar_{i}"] = False

                # =========================
                # DEFINIÇÃO CARD
                # =========================
                if row["Tipo"] == "Jogador":
                    classe = "card-jogador-turno" if i == turno_idx else "card-jogador"
                    emoji = "🤙"
                    status = "💀 Caído" if hp <= 0 else ""

                    hp_max = row["HP"] if row["HP"] else 0
                    coracao = "💙" if hp > hp_max else "❤️"

                    conteudo = f"🛡️ {row['CA']} | {coracao} {hp} {status}"

                else:
                    classe = "card-inimigo-turno" if i == turno_idx else "card-inimigo"
                    emoji = "👾"

                    hp_max = row["HP"] if row["HP"] else 0

                    if hp > hp_max:
                        conteudo = f"🛡️ {row['CA']} | 💙 {hp}"
                    else:
                        conteudo = f"🛡️ {row['CA']} | ❤️ {hp}"

                # =========================
                # BOTÕES SOBRE O CARD
                # =========================
                col_overlay = st.columns([1,1,8])

                with col_overlay[0]:
                    if st.button("⬆️", key=f"up_{i}"):
                        mover_posicao(i, -1)
                        st.rerun()

                with col_overlay[1]:
                    if st.button("⬇️", key=f"down_{i}"):
                        mover_posicao(i, 1)
                        st.rerun()

                # =========================
                # CARD
                # =========================
                st.markdown(f"""
                <div class="card {classe}">
                    <div style="padding-top: 6px;">
                        {emoji} {row['Nome']}
                    </div>
                    <div>{conteudo}</div>
                </div>
                """, unsafe_allow_html=True)

                # =========================
                # CONTROLE DE HP
                # =========================
                col_hp_a, col_hp_b, col_hp_c = st.columns([1,1,1])

                with col_hp_a:
                    if st.button("➖", key=f"hp_minus_{i}"):
                        st.session_state["hp_editavel"][i] = hp - 1
                        remover_se_morto(i)
                        st.rerun()

                with col_hp_b:
                    if st.button("-5", key=f"hp_minus5_{i}"):
                        st.session_state["hp_editavel"][i] = hp - 5
                        remover_se_morto(i)
                        st.rerun()

                with col_hp_c:
                    if st.button("➕", key=f"hp_plus_{i}"):
                        st.session_state["hp_editavel"][i] += 1
                        st.rerun()

                # =========================
                # BOTÃO CONFIG
                # =========================
                st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)

                if st.button("⚙️", key=f"btn_{i}"):
                    st.session_state[f"mostrar_{i}"] = not st.session_state[f"mostrar_{i}"]

                st.markdown("</div>", unsafe_allow_html=True)

                # =========================
                # CONDIÇÕES
                # =========================
                if st.session_state[f"mostrar_{i}"]:
                    st.session_state["condicoes"][i] = st.multiselect(
                        "Condições",
                        list(CONDICOES.keys()),
                        default=st.session_state["condicoes"][i],
                        key=f"multi_{i}"
                    )

                if st.session_state["condicoes"][i]:
                    st.markdown(" ".join([
                        f"{CONDICOES[c]}"
                        for c in st.session_state["condicoes"][i]
                    ]))