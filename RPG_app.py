import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Controle de combate - D&D 5e", layout="wide")

st.title("🎲 Controle de combate - D&D 5e")

# =========================
# SIDEBAR COMPACTA
# =========================
with st.sidebar:
    st.markdown("### 🎨 Cores")

    cor_fundo = st.color_picker("", "#0e1117", label_visibility="collapsed")

    st.markdown("**Jogadores**")
    cor_jogador = st.color_picker("Normal", "#41A7F0", key="cj1")
    cor_jogador_turno = st.color_picker("Turno", "#1D4864", key="cj2")

    st.markdown("**Inimigos**")
    cor_inimigo = st.color_picker("Normal", "#F8432F", key="ci1")
    cor_inimigo_turno = st.color_picker("Turno", "#7D241A", key="ci2")

# fundo
st.markdown(f"""
<style>
.stApp {{
    background-color: {cor_fundo};
}}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÃO
# =========================
def rolar_d20():
    return random.randint(1, 20)

# =========================
# MODELO
# =========================
st.link_button("📥 Baixar modelo de Excel", "https://docs.google.com/spreadsheets/d/1tSZyBhHuPhA_PkgKPPBdXlbrqEkiAAd7/edit?usp=sharing&ouid=100882495660344764500&rtpof=true&sd=true")

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader("Envie o Excel", type=["xlsx"])

if uploaded_file:
    try:
        df_personagens = pd.read_excel(uploaded_file, sheet_name="Personagens")
        df_inimigos = pd.read_excel(uploaded_file, sheet_name="Inimigos")
    except:
        st.error("❌ Arquivo inválido")
        st.stop()

    # TABELAS
    st.subheader("📋 Personagens")
    st.dataframe(df_personagens, use_container_width=True)

    st.subheader("👾 Inimigos")
    st.dataframe(df_inimigos, use_container_width=True)

    # =========================
    # INIMIGOS MANUAIS
    # =========================
    if "inimigos_extra" not in st.session_state:
        st.session_state["inimigos_extra"] = []

    with st.form("form_inimigo"):
        nome = st.text_input("Nome inimigo")
        ini = st.number_input("Iniciativa", step=1)
        hp = st.number_input("HP", step=1)
        ca = st.number_input("CA", step=1)

        if st.form_submit_button("Adicionar") and nome:
            st.session_state["inimigos_extra"].append({
                "Nome": nome,
                "Iniciativa": ini,
                "HP": hp,
                "CA": ca,
                "DEX": 0
            })

    # =========================
    # ROLAR INICIATIVA
    # =========================
    if st.button("🎲 Rolar iniciativa"):
        resultados = []

        # Jogadores
        for _, row in df_personagens.iterrows():
            d20 = rolar_d20()
            mod = row["Iniciativa"]
            dex = row.get("DEX", 0)

            resultados.append({
                "Nome": row["Nome"],
                "Tipo": "Jogador",
                "D20": d20,
                "Iniciativa": mod,
                "DEX": dex,
                "Total": d20 + mod,
                "HP": row.get("HP", 0),
                "CA": row.get("CA", 0)
            })

        # Inimigos
        for _, row in df_inimigos.iterrows():
            d20 = rolar_d20()
            mod = row["Iniciativa"]
            dex = row.get("DEX", 0)

            resultados.append({
                "Nome": row["Nome"],
                "Tipo": "Inimigo",
                "D20": d20,
                "Iniciativa": mod,
                "DEX": dex,
                "Total": d20 + mod,
                "HP": row.get("HP", 0),
                "CA": row.get("CA", 0)
            })

        # Inimigos extras
        for inimigo in st.session_state["inimigos_extra"]:
            d20 = rolar_d20()
            mod = inimigo["Iniciativa"]
            dex = inimigo.get("DEX", 0)

            resultados.append({
                "Nome": inimigo["Nome"],
                "Tipo": "Inimigo",
                "D20": d20,
                "Mod": mod,
                "DEX": dex,
                "Total": d20 + mod,
                "HP": inimigo["HP"],
                "CA": inimigo["CA"]
            })

        # ORDENAÇÃO COM DESEMPATE POR DEX
        df_final = pd.DataFrame(resultados)\
            .sort_values(by=["Total", "DEX"], ascending=[False, False])\
            .reset_index(drop=True)
        
        # remover DEX só da visualização
        df_exibir = df_final.drop(columns=["DEX"])

        # MOSTRAR RESULTADO CORRETAMENTE (corrigido)
        st.subheader("🎲 Resultados de Iniciativa")
        st.dataframe(df_final, use_container_width=True)

        # salvar estado
        st.session_state["combate"] = df_final
        st.session_state["turno"] = 0
        st.session_state["hp_editavel"] = df_final["HP"].fillna(0).tolist()

# =========================
# COMBATE (SEM ALTERAÇÕES)
# =========================
if "combate" in st.session_state:

    df = st.session_state["combate"]
    turno_idx = st.session_state["turno"]

    st.markdown("## 🎯 Turno Atual")

    row = df.iloc[turno_idx]
    hp_atual = st.session_state["hp_editavel"][turno_idx]
    hp_max = row["HP"] if row["HP"] else 1

    if row["Tipo"] == "Jogador":
        st.markdown(f"{row['Nome']}")
        st.write(f"🛡️ CA: {row['CA']}")
    else:
        st.markdown(f"### 👾 {row['Nome']}")
        st.write(f"🛡️ CA: {row['CA']} | ❤️ {hp_atual}/{hp_max}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("➖ HP"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual - 1)
                st.rerun()

        with col2:
            if st.button("➕ HP"):
                st.session_state["hp_editavel"][turno_idx] += 1
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➡️ Próximo turno"):
            st.session_state["turno"] = (turno_idx + 1) % len(df)
    with col2:
        if st.button("⬅️ Turno anterior"):
            st.session_state["turno"] = (turno_idx - 1) % len(df)

    st.markdown("---")

    st.markdown("## ⚔️ Combate")

    num_colunas = 4
    linhas = [df[i:i+num_colunas] for i in range(0, len(df), num_colunas)]

    for linha in linhas:
        cols = st.columns(num_colunas)

        for idx_col, (_, row) in enumerate(linha.iterrows()):
            i = row.name
            hp_atual = st.session_state["hp_editavel"][i]

            if row["Tipo"] == "Jogador":
                emoji = "🤙"
                cor = cor_jogador_turno if i == turno_idx else cor_jogador
                conteudo = f"🛡️ {row['CA']}"
            else:
                emoji = "👾"
                cor = cor_inimigo_turno if i == turno_idx else cor_inimigo
                conteudo = f"🛡️ {row['CA']} | ❤️ {hp_atual}"

            with cols[idx_col]:
                st.markdown(f"""
                <div style="
                    width:100%;
                    height:100%;
                    background-color:{cor};
                    padding:1px;
                    align-items:center;
                    border-radius:10px;
                    text-align:center;
                    margin-bottom:10px;
                    padding-top: 10px;
                ">
                    <h5>{emoji} {row['Nome']}</h5>
                    <p>{conteudo}</p>
                </div>
                """, unsafe_allow_html=True)