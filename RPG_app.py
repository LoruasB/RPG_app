import streamlit as st

from components.sidebar import render_sidebar
from styles.css import aplicar_css
from components.upload import render_upload
from components.combate_ui import render_turno
from components.grid_combate import render_grid

st.set_page_config(page_title="Controle de Combate - D&D 5e", layout="wide")

st.title("🎲 Controle de Combate - D&D 5e")

cores = render_sidebar()
aplicar_css(*cores)

# Modelo
st.link_button(
    "📥 Baixar modelo de Planilha",
    "https://docs.google.com/spreadsheets/d/1tSZyBhHuPhA_PkgKPPBdXlbrqEkiAAd7/edit?usp=sharing&rtpof=true"
)

# Upload
render_upload()

# Combate
if "combate" in st.session_state:
    df = st.session_state["combate"]
    render_turno(df)
    render_grid(df)