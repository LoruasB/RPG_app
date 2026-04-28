import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Iniciativa D&D 5e", layout="wide")

st.title("🎲 Iniciativa D&D 5e")

# =========================
# CONDIÇÕES
# =========================
CONDICOES = {
    "Agarrado": "🤝",
    "Amedrontado": "😨",
    "Atordoado": "💫",
    "Caído": "🪦",
    "Cego": "🕶️",
    "Confuso": "😵",
    "Contido": "⛓️",
    "Desafiado": "⚔️",
    "Dominado": "🧠",
    "Enfeitiçado": "💖",
    "Envenenado": "☠️",
    "Escondido": "🫥",
    "Exaustão": "🥵",
    "Incapacitado": "🚫",
    "Inconsciente": "😴",
    "Invisível": "👻",
    "Marcado": "🎯",
    "Paralisado": "🧊",
    "Petrificado": "🗿",
    "Possuído": "👁️",
    "Rastreado": "👣",
    "Surdo": "🔇"
}

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
# CSS
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

.card-jogador {{
    background-color: {cor_jogador};
}}

.card-jogador-turno {{
    background-color: {cor_jogador_turno};
    border: 2px solid white;
}}

.card-inimigo {{
    background-color: {cor_inimigo};
}}

.card-inimigo-turno {{
    background-color: {cor_inimigo_turno};
    border: 2px solid white;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

div.stButton > button {
    font-size: 8px;
    padding: 2px 2px;
    border-radius: 20px;
    min-width: 25px;
}

button[kind="secondary"] {
    font-size 14px;
    padding: 6px 10px;
}

.hp-btn button {
    font-size: 12px;
    padding: 3px 6px;
    min-width: 40px;
}

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

        # remove da lista
        df = df.drop(index).reset_index(drop=True)
        hp_lista.pop(index)

        # ajusta turno
        if st.session_state["turno"] >= len(df):
            st.session_state["turno"] = 0

        st.session_state["combate"] = df
        st.session_state["hp_editavel"] = hp_lista

# =========================
# MODELO
# =========================
st.link_button(
    "📥 Baixar modelo de Planilha",
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

    if st.button("🎲 Rolar iniciativa"):
        resultados = []

        for _, row in df_personagens.iterrows():
            d20 = rolar_d20()
            resultados.append({
                "Nome": row["Nome"],
                "Tipo": "Jogador",
                "Total": d20 + row["Iniciativa"],
                "DEX": row.get("DEX", 0),
                "IniBase": row["Iniciativa"],
                "HP": row.get("HP", 0),
                "CA": row.get("CA", 0)
            })

        for _, row in df_inimigos.iterrows():
            d20 = rolar_d20()
            resultados.append({
                "Nome": row["Nome"],
                "Tipo": "Inimigo",
                "Total": d20 + row["Iniciativa"],
                "DEX": row.get("DEX", 0),
                "IniBase": row["Iniciativa"],
                "HP": row.get("HP", 0),
                "CA": row.get("CA", 0)
            })

        for inimigo in st.session_state["inimigos_extra"]:
            d20 = rolar_d20()
            resultados.append({
                "Nome": inimigo["Nome"],
                "Tipo": "Inimigo",
                "Total": d20 + inimigo["Iniciativa"],
                "DEX": inimigo["DEX"],
                "IniBase": inimigo["Iniciativa"],
                "HP": inimigo["HP"],
                "CA": inimigo["CA"]
            })

        df_final = pd.DataFrame(resultados)\
            .sort_values(by=["Total", "DEX", "IniBase"], ascending=[False, False, False])\
            .reset_index(drop=True)

        st.subheader("🎲 Resultados de Iniciativa")
        st.dataframe(df_final.drop(columns=["DEX", "IniBase"]), use_container_width=True)

        st.session_state["combate"] = df_final
        st.session_state["turno"] = 0
        st.session_state["rodada"] = 1
        st.session_state["hp_editavel"] = df_final["HP"].fillna(0).tolist()
        st.session_state["condicoes"] = [[] for _ in range(len(df_final))]
        
# =========================
# COMBATE
# =========================
if "combate" in st.session_state:

    df = st.session_state["combate"]
    turno_idx = st.session_state["turno"]
    
    # ==============================
    # CONTROLE DE TURNO e RODADA
    # ==============================

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

    # =========================
    # HP INIMIGOS
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

            with cols[idx_col]:

                if f"mostrar_{i}" not in st.session_state:
                    st.session_state[f"mostrar_{i}"] = False

                # card
                if row["Tipo"] == "Jogador":
                    classe = "card-jogador-turno" if i == turno_idx else "card-jogador"
                    emoji = "🤙"
                    conteudo = f"🛡️ {row['CA']}"
                else:
                    classe = "card-inimigo-turno" if i == turno_idx else "card-inimigo"
                    emoji = "👾"
                    conteudo = f"🛡️ {row['CA']} | ❤️ {hp}"

                st.markdown(f"""
                <div class="card {classe}">
                    <div>{emoji} {row['Nome']}</div>
                    <div>{conteudo}</div>
                </div>
                """, unsafe_allow_html=True)

                # botão engrenagem
                st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)

                if st.button("⚙️", key=f"btn_{i}"):
                    st.session_state[f"mostrar_{i}"] = not st.session_state[f"mostrar_{i}"]

                st.markdown("</div>", unsafe_allow_html=True)

                # condições
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
