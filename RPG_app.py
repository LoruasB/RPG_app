import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Iniciativa D&D 5e", layout="wide")

st.title("🎲 Iniciativa D&D 5e")

# =========================
# SIDEBAR
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

# =========================
# CSS GLOBAL
# =========================
st.markdown(f"""
<style>
.stApp {{
    background-color: {cor_fundo};
}}

.card {{
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÕES
# =========================
def rolar_d20():
    return random.randint(1, 20)

def remover_se_morto(index):
    df = st.session_state["combate"]
    hp_lista = st.session_state["hp_editavel"]

    if df.loc[index, "Tipo"] == "Inimigo" and hp_lista[index] <= 0:

        nome = df.loc[index, "Nome"]

        df = df.drop(index).reset_index(drop=True)
        hp_lista.pop(index)

        if st.session_state["turno"] >= len(df):
            st.session_state["turno"] = 0

        st.session_state["combate"] = df
        st.session_state["hp_editavel"] = hp_lista

        st.warning(f"💀 {nome} foi derrotado!")

# =========================
# MODELO
# =========================
st.link_button(
    "📥 Baixar modelo de Excel",
    "https://docs.google.com/spreadsheets/d/1tSZyBhHuPhA_PkgKPPBdXlbrqEkiAAd7/edit?usp=sharing&rtpof=true"
)

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader("Envie o Excel", type=["xlsx"])

if uploaded_file:
    try:
        excel = pd.ExcelFile(uploaded_file)

        df_personagens = pd.read_excel(excel, sheet_name="Personagens")
        df_inimigos = pd.read_excel(excel, sheet_name="Inimigos")

        df_personagens.columns = df_personagens.columns.str.strip()
        df_inimigos.columns = df_inimigos.columns.str.strip()

    except Exception as e:
        st.error(f"❌ Erro ao ler arquivo: {e}")
        st.stop()

    st.subheader("📋 Personagens")
    st.dataframe(df_personagens, use_container_width=True)

    st.subheader("👾 Inimigos")
    st.dataframe(df_inimigos, use_container_width=True)

    # =========================
    # ROLAR INICIATIVA
    # =========================
    if st.button("🎲 Rolar iniciativa"):
        resultados = []

        for _, row in df_personagens.iterrows():
            d20 = rolar_d20()
            resultados.append({
                "Nome": row["Nome"],
                "Tipo": "Jogador",
                "DEX": row.get("DEX", 0),
                "Total": d20 + row["Iniciativa"],
                "HP": row.get("HP", 0),
                "CA": row.get("CA", 0)
            })

        for _, row in df_inimigos.iterrows():
            d20 = rolar_d20()
            resultados.append({
                "Nome": row["Nome"],
                "Tipo": "Inimigo",
                "DEX": row.get("DEX", 0),
                "Total": d20 + row["Iniciativa"],
                "HP": row.get("HP", 0),
                "CA": row.get("CA", 0)
            })

        df_final = pd.DataFrame(resultados)\
            .sort_values(by=["Total", "DEX"], ascending=[False, False])\
            .reset_index(drop=True)

        st.subheader("🎲 Resultados de Iniciativa")
        st.dataframe(df_final.drop(columns=["DEX"]), use_container_width=True)

        st.session_state["combate"] = df_final
        st.session_state["turno"] = 0
        st.session_state["rodada"] = 1
        st.session_state["hp_editavel"] = df_final["HP"].fillna(0).tolist()

# =========================
# COMBATE
# =========================
if "combate" in st.session_state:

    df = st.session_state["combate"]
    turno_idx = st.session_state["turno"]

    st.markdown(f"## 🔁 Rodada {st.session_state['rodada']}")
    st.markdown("## 🎯 Turno Atual")

    row = df.iloc[turno_idx]
    hp_atual = st.session_state["hp_editavel"][turno_idx]
    hp_max = row["HP"] if row["HP"] else 1

    # =========================
    # LINHA TURNO
    # =========================
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
        st.markdown(f"<h3 style='text-align:center;'>🎯 {row['Nome']}</h3>", unsafe_allow_html=True)

    with col3:
        if st.button("▶", key="next_turn"):
            if turno_idx == len(df) - 1:
                st.session_state["turno"] = 0
                st.session_state["rodada"] += 1
            else:
                st.session_state["turno"] += 1
            st.rerun()

    # =========================
    # HP INIMIGO
    # =========================
    if row["Tipo"] == "Inimigo":

        col_hp1, col_hp2, col_hp3, col_hp4, col_hp5 = st.columns([1,1,2,1,1])

        with col_hp1:
            if st.button("➖", key="hp_minus"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual - 1)
                remover_se_morto(turno_idx)
                st.rerun()

        with col_hp2:
            if st.button("-5", key="hp_minus5"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual - 5)
                remover_se_morto(turno_idx)
                st.rerun()

        with col_hp3:
            proporcao = hp_atual / hp_max if hp_max > 0 else 0

            # barra de vida
            st.progress(proporcao)
            
            # cor dinâmica
            if proporcao > 0.6:
                cor_texto = "🟢"
            elif proporcao > 0.3:
                cor_texto = "🟡"
            else:
                cor_texto = "🔴"

            st.markdown(
                f"<div style='text-align:center;'>{cor_texto} {hp_atual}/{hp_max}</div>",
                unsafe_allow_html=True
            )
                
        with col_hp4:
            if st.button("+5", key="hp_plus5"):
                st.session_state["hp_editavel"][turno_idx] = max(0, hp_atual + 5)
                remover_se_morto(turno_idx)
                st.rerun()
                
        with col_hp5:
            if st.button("➕", key="hp_plus"):
                st.session_state["hp_editavel"][turno_idx] += 1
                st.rerun()

    st.markdown("---")

    # =========================
    # GRID COMBATE
    # =========================
    st.markdown("## ⚔️ Combate")

    num_colunas = 4
    linhas = [df[i:i+num_colunas] for i in range(0, len(df), num_colunas)]

    for linha in linhas:
        cols = st.columns(num_colunas)

        for idx_col, (_, row) in enumerate(linha.iterrows()):
            i = row.name
            hp = st.session_state["hp_editavel"][i]

            if row["Tipo"] == "Jogador":
                emoji = "🤙"
                cor = cor_jogador_turno if i == turno_idx else cor_jogador
                conteudo = f"🛡️ {row['CA']}"
            else:
                emoji = "👾"
                cor = cor_inimigo_turno if i == turno_idx else cor_inimigo
                conteudo = f"🛡️ {row['CA']} | ❤️ {hp}"

            with cols[idx_col]:
                st.markdown(f"""
                <div style="
                    background-color:{cor};
                    padding:10px;
                    border-radius:10px;
                    text-align:center;
                    margin-bottom:10px;
                ">
                    <b>{emoji} {row['Nome']}</b><br>
                    {conteudo}
                </div>
                """, unsafe_allow_html=True)