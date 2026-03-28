"""
components/styles.py — CSS global (compatível com Streamlit; não usar pasta pages/ para views).
"""

import streamlit as st


def injetar_css():
    # Fontes via <link> — @import dentro de <style> costuma falhar no app Streamlit
    st.markdown(
        "<link rel='stylesheet' "
        "href='https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800"
        "&family=DM+Sans:wght@400;500;600&display=swap'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<style>
  /* App shell — sem sobrescrever todo div (isso quebrava hero/banners escuros) */
  [data-testid="stAppViewContainer"] {
    background-color: #F5F7FA !important;
  }
  .stApp {
    font-family: 'DM Sans', system-ui, sans-serif !important;
    color: #1A202C !important;
  }

  /* Texto padrão do markdown Streamlit — alvo específico */
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] ol,
  [data-testid="stMarkdownContainer"] ul {
    color: #1A202C !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
  }
  [data-testid="stMarkdownContainer"] strong {
    color: #0F172A !important;
    font-weight: 600 !important;
  }

  [data-testid="stWidgetLabel"] label,
  [data-testid="stWidgetLabel"] p,
  label[data-testid="stWidgetLabel"] {
    color: #2D3748 !important;
  }

  h1, h2, h3 {
    font-family: 'Sora', system-ui, sans-serif !important;
    color: #0F2027 !important;
  }

  /* Botões */
  .stButton > button {
    background-color: #FFFFFF !important;
    color: #1A202C !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
  }
  .stButton > button[kind="primary"],
  .stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #203A43, #2C5364) !important;
    color: #FFFFFF !important;
    border: none !important;
  }
  
  .stButton > button p, .stButton > button span {
    color: inherit !important;
  }

  /* Inputs fortes para sobrepor o tema (barras de URL e campos de texto) */
  div[data-testid="stTextInput"] div[data-baseweb="base-input"],
  div[data-testid="stTextArea"] div[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 8px !important;
  }
  div[data-testid="stTextInput"] input,
  div[data-testid="stTextArea"] textarea {
    color: #1A202C !important;
    background-color: transparent !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
  }
  div[data-testid="stTextInput"] input::placeholder,
  div[data-testid="stTextArea"] textarea::placeholder {
    color: #A0AEC0 !important;
    opacity: 1 !important;
  }

  .stSelectbox [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1A202C !important;
  }

  .stTabs [data-baseweb="tab-panel"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #1A202C !important;
  }
  .stTabs [data-baseweb="tab"] {
    color: #4A5568 !important;
    font-weight: 600 !important;
  }

  [data-testid="stAlert"] p {
    color: #1A202C !important;
  }

  .stDownloadButton > button {
    background: #FFFFFF !important;
    border: 1px solid #2C5364 !important;
    color: #2C5364 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
  }
  .stDownloadButton > button:hover {
    background: #2C5364 !important;
    color: #FFFFFF !important;
  }



  /* Blocos HTML custom — garantir contraste */
  .na-hero, .na-hero h2, .na-hero p, .na-hero strong, .na-hero span.na-hero-muted {
    color: #F8FAFC !important;
  }
  .na-hero span.na-hero-tag {
    color: #E0F2FE !important;
  }

  .header-banner {
    background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
    border-radius: 14px;
    padding: 22px 28px;
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
    color: #F8FAFC !important;
  }
  .header-banner h1 {
    margin: 0;
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF !important;
    font-family: 'Sora', sans-serif;
  }
  .header-banner .header-icon { font-size: 44px; line-height: 1; flex-shrink: 0; }
  .header-banner .header-text p {
    margin: 6px 0 0;
    color: #C8E0EA !important;
    font-size: 14px !important;
    line-height: 1.45 !important;
  }

  .stApp .sidebar-title { font-size: 17px; font-weight: 700; color: #FFFFFF !important; font-family: 'Sora', sans-serif; }
  .stApp .sidebar-sub { font-size: 12px; color: #94B4C8 !important; }
  .stApp .sb-section {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #7BA8BC !important; margin: 8px 0 6px; display: block;
  }
  .stApp .status-ok {
    background: #0D3B1A; border: 1px solid #1A6B31; border-radius: 8px;
    padding: 8px 12px; font-size: 13px; color: #86EFAC !important; font-weight: 600;
  }
  .stApp .status-err {
    background: #3B0D0D; border: 1px solid #6B1A1A; border-radius: 8px;
    padding: 8px 12px; font-size: 13px; color: #FCA5A5 !important; font-weight: 600;
  }
  .stApp .hist-item {
    background: #1E3A47; border-radius: 8px; padding: 8px 10px;
    margin: 4px 0; display: flex; justify-content: space-between; align-items: center; gap: 8px;
  }
  .stApp .hist-title { font-size: 11px; color: #C8E0EA !important; flex: 1; line-height: 1.35; }
  .stApp .hist-badge { font-size: 10px; font-weight: 700; white-space: nowrap; }

  .stApp .section-title {
    font-size: 17px; font-weight: 700; color: #0F2027 !important;
    font-family: 'Sora', sans-serif;
    border-left: 4px solid #2C5364; padding-left: 12px; margin: 20px 0 14px;
  }
  .stApp .tab-desc { font-size: 14px; color: #475569 !important; margin: 0 0 14px; }

  .stApp .noticia-preview {
    background: #FFFFFF; border: 1px solid #E2E8F0;
    border-left: 5px solid #2C5364; border-radius: 10px;
    padding: 18px 22px; margin: 12px 0;
  }
  .stApp .np-titulo { font-size: 16px; font-weight: 700; color: #0F2027 !important; font-family: 'Sora', sans-serif; margin-bottom: 6px; }
  .stApp .np-fonte { font-size: 13px; color: #64748B !important; margin-bottom: 10px; }
  .stApp .np-preview { font-size: 14px; color: #334155 !important; line-height: 1.75; border-top: 1px solid #F1F5F9; padding-top: 10px; }

  .stApp .news-item {
    background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
    padding: 12px 16px; margin: 4px 0; line-height: 1.45;
  }
  .stApp .news-item strong { color: #0F2027 !important; }
  .stApp .news-item span { color: #64748B !important; }

  .stApp .result-sentiment-card {
    border-radius: 12px; padding: 22px 26px; margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }
  .stApp .rs-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; font-family: 'Sora', sans-serif; }
  .stApp .rs-value { font-size: 28px; font-weight: 800; font-family: 'Sora', sans-serif; margin-bottom: 4px; }
  .stApp .rs-confianca { font-size: 13px; opacity: 0.9; margin-bottom: 12px; }
  .stApp .rs-justificativa { font-size: 14px; line-height: 1.7; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 12px; margin-top: 4px; }

  .stApp .card-positivo { background: linear-gradient(135deg, #E8F5E9, #F1FAF2); border: 1px solid #A5D6A7; color: #1B5E20 !important; }
  .stApp .card-negativo { background: linear-gradient(135deg, #FFEBEE, #FFF5F6); border: 1px solid #EF9A9A; color: #B71C1C !important; }
  .stApp .card-neutro   { background: linear-gradient(135deg, #FFF8E1, #FFFDF0); border: 1px solid #FFD54F; color: #E65100 !important; }
  .stApp .card-positivo * { color: #1B5E20 !important; }
  .stApp .card-negativo * { color: #B71C1C !important; }
  .stApp .card-neutro   * { color: #E65100 !important; }

  .stApp .result-box {
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
    padding: 22px 26px; margin-bottom: 16px;
  }
  .stApp .rb-title { font-size: 15px; font-weight: 700; color: #0F2027 !important; font-family: 'Sora', sans-serif; margin-bottom: 12px; }
  .stApp .rb-content { font-size: 15px !important; color: #334155 !important; line-height: 1.8 !important; }

  .stApp .keyword-badge {
    display: inline-block; background: #EDF2F7; border: 1px solid #CBD5E0;
    border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600;
    color: #2D3748 !important; margin: 3px;
  }
  .stApp .topico-badge {
    display: inline-block; background: #EBF8FF; border: 1px solid #90CDF4;
    border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600;
    color: #2C5282 !important; margin: 3px;
  }

  .stApp .welcome-box {
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px;
    padding: 36px; text-align: center; margin: 20px 0;
  }
  .stApp .welcome-box .wb-icon { font-size: 44px; margin-bottom: 10px; line-height: 1; }
  .stApp .welcome-box h3 { color: #0F2027 !important; font-family: 'Sora', sans-serif; font-size: 22px; }
  .stApp .welcome-box p { color: #475569 !important; font-size: 15px !important; line-height: 1.65 !important; }

  .stApp .feature-card {
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
    padding: 22px; text-align: center; height: 100%;
  }
  .stApp .fc-icon { font-size: 28px; margin-bottom: 8px; line-height: 1; }
  .stApp .fc-title { display: block; font-size: 15px; color: #0F2027 !important; font-family: 'Sora', sans-serif; margin-bottom: 6px; }
  .stApp .fc-desc { font-size: 14px !important; color: #475569 !important; line-height: 1.6 !important; margin: 0 !important; }

  .stApp .tech-footer { text-align: center; color: #64748B !important; font-size: 13px !important; padding: 20px 0 10px; }

  /* Navegação principal na sidebar */
  .na-nav-wrap {
    background: #162A32;
    border: 1px solid #2C5364;
    border-radius: 12px;
    padding: 12px 10px 14px;
    margin-bottom: 8px;
  }
  .na-nav-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7BA8BC !important;
    margin-bottom: 10px;
    font-family: 'Sora', sans-serif;
  }
</style>
""",
        unsafe_allow_html=True,
    )
