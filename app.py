"""
app.py — Entrada única do Streamlit (NÃO use a pasta `pages/` para telas: o framework
reserva esse nome e cria rotas automáticas, conflitando com o roteador manual).

Estrutura:
  app.py → session_state + barra lateral de navegação
  views/home.py, views/analyzer.py → telas
  pipeline/, providers/, services/, components/, utils/
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from components.styles import injetar_css

load_dotenv(Path(__file__).resolve().parent / ".env")

st.set_page_config(
    page_title="NewsAnalyzer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

injetar_css()

defaults = {
    "pagina_atual": "home",
    "resultado": None,
    "noticia_atual": None,
    "historico": [],
    "resultados_busca": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def navegar(pagina: str):
    st.session_state["pagina_atual"] = pagina
    st.rerun()


pagina = st.session_state["pagina_atual"]

# ─── Navegação global (sidebar) — sempre no topo ─────────────────────────────
with st.sidebar:
    st.markdown("### NewsAnalyzer")
    st.caption("PLN · Sabiá-4 · FIAP")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Projeto",
            use_container_width=True,
            type="primary" if pagina == "home" else "secondary",
            key="nav_home",
        ):
            if pagina != "home":
                navegar("home")
    with c2:
        if st.button(
            "Análise PLN",
            use_container_width=True,
            type="primary" if pagina == "analisador" else "secondary",
            key="nav_analisador",
        ):
            if pagina != "analisador":
                navegar("analisador")
    st.divider()

# ─── Conteúdo da rota ────────────────────────────────────────────────────────
if pagina == "home":
    from views.home import renderizar_home

    renderizar_home(navegar)

elif pagina == "analisador":
    from views.analyzer import renderizar_analisador

    renderizar_analisador(navegar)

else:
    st.error(f"Rota desconhecida: {pagina!r}")
    if st.button("Voltar ao projeto"):
        navegar("home")
