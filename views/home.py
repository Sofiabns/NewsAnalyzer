"""
views/home.py — Tela inicial: projeto, integrantes, arquitetura.
"""

import streamlit as st


def renderizar_home(navegar):
    """Renderiza a tela inicial."""

    # Sidebar: texto legível e nativo
    with st.sidebar:
        st.markdown('<span class="sb-section">Sobre o app</span>', unsafe_allow_html=True)
        st.write(
            "O **NewsAnalyzer** usa PLN (modelo **Sabiá-4**, Maritaca AI) para classificar "
            "o sentimento de notícias e gerar **resumos automáticos**."
        )
        st.divider()
        st.markdown('<span class="sb-section">Disciplina</span>', unsafe_allow_html=True)
        st.caption("Natural Language Processing · FIAP · 2026")

    # Cabeçalho
    st.markdown(
        """
    <div class="header-banner">
      <div class="header-icon">📰</div>
      <div class="header-text">
        <h1>NewsAnalyzer</h1>
        <p>Notícias · Sentimento · Resumo automático · PLN</p>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Hero — classe na-hero garante texto claro sobre fundo escuro (CSS dedicado)
    st.markdown(
        """
    <div class="na-hero" style="
        background:linear-gradient(135deg,#0F2027 0%,#203A43 55%,#2C5364 100%);
        border-radius:16px; padding:40px 32px; text-align:center;
        margin-bottom:28px; box-shadow:0 8px 32px rgba(0,0,0,0.18);
    ">
        <div style="font-size:48px;margin-bottom:12px;">🧠</div>
        <h2 style="font-family:Sora,sans-serif;font-size:clamp(1.15rem,2.5vw,1.5rem);
            font-weight:800;margin:0 0 14px;letter-spacing:-0.02em;line-height:1.25;">
            Processamento de Linguagem Natural aplicado ao jornalismo
        </h2>
        <p class="na-hero-muted" style="font-size:15px;max-width:640px;margin:0 auto 22px;line-height:1.75;">
            Extração de notícias (URL ou texto), análise de sentimento e resumo inteligente com
            <strong>Sabiá-4</strong> (Maritaca AI).
        </p>
        <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;">
            <span class="na-hero-tag" style="background:rgba(255,255,255,0.12);
                border:1px solid rgba(255,255,255,0.2);border-radius:999px;
                padding:6px 14px;font-size:12px;font-weight:600;">Python</span>
            <span class="na-hero-tag" style="background:rgba(255,255,255,0.12);
                border:1px solid rgba(255,255,255,0.2);border-radius:999px;
                padding:6px 14px;font-size:12px;font-weight:600;">Streamlit</span>
            <span class="na-hero-tag" style="background:rgba(255,255,255,0.12);
                border:1px solid rgba(255,255,255,0.2);border-radius:999px;
                padding:6px 14px;font-size:12px;font-weight:600;">Sabiá-4</span>
            <span class="na-hero-tag" style="background:rgba(255,255,255,0.12);
                border:1px solid rgba(255,255,255,0.2);border-radius:999px;
                padding:6px 14px;font-size:12px;font-weight:600;">NLP</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_feat, col_team = st.columns([1.1, 1], gap="large")

    with col_feat:
        st.markdown('<div class="section-title">O que o sistema faz</div>', unsafe_allow_html=True)

        funcionalidades = [
            ("🔗", "Extração por URL",
             "Título e corpo do artigo com <strong>newspaper3k</strong> e <strong>BeautifulSoup4</strong>."),
            ("📝", "Texto manual",
             "Cole o texto da notícia quando não houver URL."),
            ("🔍", "Busca por tema",
             "Google News RSS (pt / en / es)."),
            ("💬", "Sentimento",
             "Positivo, negativo ou neutro, com justificativa."),
            ("📋", "Resumo",
             "Breve, padrão ou detalhado — palavras-chave e tópicos."),
            ("📊", "Histórico",
             "Sessão atual em DataFrame, filtros e export CSV/JSON."),
        ]

        for icon, titulo, desc in funcionalidades:
            st.markdown(
                f"""
            <div style="display:flex;gap:14px;align-items:flex-start;
                background:#ffffff;border:1px solid #E2E8F0;border-radius:12px;
                padding:15px 18px;margin-bottom:10px;
                box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                <div style="font-size:22px;line-height:1;flex-shrink:0;padding-top:2px;">{icon}</div>
                <div>
                    <div style="font-size:15px;font-weight:700;color:#0F2027;
                        font-family:Sora,sans-serif;margin-bottom:4px;">{titulo}</div>
                    <div style="font-size:14px;color:#475569;line-height:1.65;">{desc}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col_team:
        st.markdown('<div class="section-title">Integrantes</div>', unsafe_allow_html=True)

        integrantes = [
            ("Sofia Bueris Netto de Souza", "RM565818"),
            ("Vinícius Adrian Siqueira de Oliveira", "RM564962"),
            ("Augusto Oliveira Codo de Sousa", "RM562080"),
            ("Felipe de Oliveira Cabral", "RM561720"),
            ("Gabriel Tonelli Avelino Dos Santos", "RM564705"),
        ]

        for i, (nome, rm) in enumerate(integrantes):
            st.markdown(
                f"""
            <div style="background:#ffffff;border:1px solid #E2E8F0;border-radius:12px;
                padding:14px 18px;margin-bottom:10px;
                box-shadow:0 2px 6px rgba(0,0,0,0.04);
                display:flex;align-items:center;gap:14px;">
                <div style="width:38px;height:38px;flex-shrink:0;
                    background:linear-gradient(135deg,#203A43,#2C5364);
                    border-radius:50%;display:flex;align-items:center;justify-content:center;
                    font-size:15px;font-weight:800;color:#ffffff;font-family:Sora,sans-serif;">
                    {i + 1}
                </div>
                <div>
                    <div style="font-size:14px;font-weight:700;color:#0F2027;
                        font-family:Sora,sans-serif;line-height:1.3;">{nome}</div>
                    <div style="font-size:12px;color:#64748B;margin-top:3px;font-weight:600;">{rm}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """<div style="background:linear-gradient(135deg,#0F2027,#2C5364);border-radius:12px;padding:18px 20px;margin-top:6px;text-align:center;">
<p style="font-size:11px;color:#94B4C8!important;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin:0 0 8px 0;">Disciplina</p>
<p style="font-size:16px;color:#ffffff!important;font-weight:700;font-family:Sora,sans-serif;margin:0;">Natural Language Processing</p>
<p style="font-size:13px;color:#B8D4E3!important;margin:6px 0 0 0;">FIAP · 2026</p>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Arquitetura</div>', unsafe_allow_html=True)

    arch = [
        ("📄", "app.py", "Roteamento por <code>session_state</code> (uma entrada Streamlit)."),
        ("🖥️", "views/", "<strong>home.py</strong> e <strong>analyzer.py</strong> — telas (pasta não é <code>pages/</code>)."),
        ("⚙️", "pipeline/ + providers/", "<strong>news_pipeline.py</strong> + <strong>maritaca_pln.py</strong> (Sabiá-4)."),
        ("🌐", "services/", "<strong>news_fetcher.py</strong> — URL e RSS."),
        ("🧩", "components/", "<strong>result_card.py</strong>, <strong>styles.py</strong>."),
    ]

    cols = st.columns(5, gap="small")
    for col, (icon, nome, desc) in zip(cols, arch):
        with col:
            st.markdown(
                f"""
            <div style="background:#ffffff;border:1px solid #E2E8F0;border-radius:12px;
                padding:18px 12px;text-align:center;height:100%;
                box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="font-size:26px;margin-bottom:8px;">{icon}</div>
                <div style="font-size:13px;font-weight:700;color:#0F2027;
                    font-family:Sora,sans-serif;margin-bottom:6px;">{nome}</div>
                <div style="font-size:11px;color:#475569;line-height:1.55;">{desc}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("Abrir análise de notícias →", use_container_width=True, type="primary"):
            navegar("analisador")

    st.markdown(
        """
    <div class="tech-footer" style="margin-top:20px;">
        Python · Streamlit · Sabiá-4 (Maritaca AI) · BeautifulSoup · newspaper3k
    </div>
    """,
        unsafe_allow_html=True,
    )
