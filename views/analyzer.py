"""
views/analyzer.py — Tela de análise (entrada, PLN, resultados, histórico).
"""

import html
import json
import os

import pandas as pd
import streamlit as st

from components.result_card import renderizar_resultado
from pipeline.news_pipeline import executar_analise_pln
from services.news_fetcher import buscar_por_tema, buscar_por_url
from utils.text_cleaner import extrair_titulo


def renderizar_analisador(navegar):
    """Renderiza a tela do analisador."""

    api_key = os.getenv("MARITACA_API_KEY", "")

    with st.sidebar:
        st.markdown('<span class="sb-section">Status da API</span>', unsafe_allow_html=True)
        if api_key:
            st.markdown('<div class="status-ok">Modelo Sabiá-4 pronto</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-err">Defina MARITACA_API_KEY no .env</div>', unsafe_allow_html=True)
            st.caption("Sem a chave, a análise PLN não roda.")

        st.divider()
        st.markdown('<span class="sb-section">Parâmetros</span>', unsafe_allow_html=True)

        idioma = st.selectbox(
            "Idioma da notícia",
            ["Automático", "Português", "Inglês", "Espanhol"],
            help="Opcional: o modelo também infere o idioma.",
        )

        profundidade = st.select_slider(
            "Profundidade do resumo",
            options=["Breve", "Padrão", "Detalhado"],
            value="Padrão",
            help="Breve: poucas frases · Padrão: um parágrafo · Detalhado: mais contexto",
        )

        st.divider()

        if st.session_state.historico:
            st.markdown('<span class="sb-section">Últimas análises</span>', unsafe_allow_html=True)
            for item in reversed(st.session_state.historico[-5:]):
                cor = {"Positivo": "#4ADE80", "Negativo": "#F87171", "Neutro": "#FBBF24"}.get(
                    item.get("sentimento", ""), "#94A3B8"
                )
                st.markdown(
                    f'<div class="hist-item">'
                    f'<span class="hist-title">{item.get("titulo", "")[:36]}…</span>'
                    f'<span class="hist-badge" style="color:{cor}!important;">'
                    f'{item.get("sentimento", "?")}</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
            if st.button("Limpar histórico", use_container_width=True):
                st.session_state.historico = []
                st.rerun()

    st.markdown(
        """
    <div class="header-banner">
      <div class="header-icon">📰</div>
      <div class="header-text">
        <h1>Análise de notícias</h1>
        <p>Sentimento · Score · Resumo (Sabiá-4)</p>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">1 · Entrada da notícia</div>',
        unsafe_allow_html=True,
    )

    tab_url, tab_texto, tab_busca = st.tabs(
        [
            "URL",
            "Texto",
            "Busca por tema",
        ]
    )

    noticia_para_processar = None

    with tab_url:
        st.markdown('<p class="tab-desc">Cole a URL de um portal de notícias.</p>', unsafe_allow_html=True)
        url_input = st.text_input(
            "URL",
            placeholder="https://…",
            label_visibility="collapsed",
        )
        col_btn, col_ex = st.columns([1, 3])
        with col_btn:
            btn_url = st.button("Carregar", use_container_width=True, key="btn_url")
        with col_ex:
            st.caption("Ex.: G1, BBC, UOL, CNN, Folha…")

        if btn_url and url_input:
            with st.spinner("Extraindo a notícia…"):
                resultado_url = buscar_por_url(url_input)
            if resultado_url.get("erro"):
                st.error(f"❌ {resultado_url['erro']}")
            else:
                noticia_para_processar = resultado_url
                st.success(f"Carregado: **{resultado_url.get('titulo', '')[:80]}**")
        elif btn_url:
            st.warning("Informe uma URL.")

    with tab_texto:
        st.markdown('<p class="tab-desc">Cole o texto completo da notícia.</p>', unsafe_allow_html=True)
        titulo_manual = st.text_input(
            "Título (opcional)",
            placeholder="Ex.: Governo anuncia…",
        )
        texto_input = st.text_area(
            "Texto da notícia",
            placeholder="Cole o conteúdo aqui…",
            height=260,
        )
        col_info, col_btn2 = st.columns([3, 1])
        with col_info:
            if texto_input:
                st.caption(f"{len(texto_input.split())} palavras · {len(texto_input)} caracteres")
            else:
                st.caption("Recomendado: pelo menos ~100 palavras para melhor resultado.")
        with col_btn2:
            btn_texto = st.button("Usar texto", use_container_width=True, key="btn_texto")

        if btn_texto and texto_input:
            if len(texto_input.split()) < 20:
                st.warning("Texto curto — use pelo menos ~20 palavras.")
            else:
                titulo = titulo_manual if titulo_manual else extrair_titulo(texto_input)
                noticia_para_processar = {
                    "titulo": titulo,
                    "texto": texto_input,
                    "fonte": "Texto colado",
                    "url": None,
                }
                st.success(f"Texto definido: **{titulo[:80]}**")
        elif btn_texto:
            st.warning("Cole o texto da notícia.")

    with tab_busca:
        st.markdown('<p class="tab-desc">Busca no Google News (RSS).</p>', unsafe_allow_html=True)
        col_q, col_lang = st.columns([3, 1])
        with col_q:
            query_input = st.text_input(
                "Tema",
                placeholder="Ex.: inteligência artificial, economia…",
                label_visibility="collapsed",
            )
        with col_lang:
            lang_map = {"pt-BR": "Português", "en-US": "Inglês", "es-419": "Espanhol"}
            idioma_busca = st.selectbox(
                "Idioma",
                options=list(lang_map.keys()),
                format_func=lambda x: lang_map[x],
                label_visibility="collapsed",
            )
        col_n, col_btn3 = st.columns([3, 1])
        with col_n:
            n_resultados = st.slider("Quantidade", 1, 10, 5)
        with col_btn3:
            st.markdown("<br>", unsafe_allow_html=True)
            btn_busca = st.button("Buscar", use_container_width=True, key="btn_busca")

        if btn_busca and query_input:
            with st.spinner(f"Buscando “{query_input}”…"):
                st.session_state["resultados_busca"] = buscar_por_tema(
                    query_input, idioma=idioma_busca, max_resultados=n_resultados
                )
        elif btn_busca:
            st.warning("Digite um termo de busca.")

        if st.session_state.get("resultados_busca") is not None:
            resultados_busca = st.session_state["resultados_busca"]
            if not resultados_busca:
                st.warning("Nenhum resultado. Tente outro termo.")
            else:
                st.success(f"{len(resultados_busca)} resultado(s).")
                st.markdown("**Escolha uma notícia:**")
                for i, noticia_item in enumerate(resultados_busca):
                    col_sel, col_info_n = st.columns([1, 6])
                    with col_sel:
                        if st.button("Analisar →", key=f"sel_{i}", use_container_width=True):
                            st.session_state["noticia_atual"] = noticia_item
                            st.session_state["resultado"] = None
                            st.session_state["resultados_busca"] = None
                            st.rerun()
                    with col_info_n:
                        st.markdown(
                            f'<div class="news-item">'
                            f'<strong>{noticia_item.get("titulo", "")[:100]}</strong><br>'
                            f'<span style="color:#64748B;font-size:12px">'
                            f'{noticia_item.get("fonte", "?")} · {noticia_item.get("data", "")}</span>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )

    if noticia_para_processar:
        st.session_state["noticia_atual"] = noticia_para_processar

    noticia = st.session_state.get("noticia_atual")

    if noticia:
        st.markdown("---")
        st.markdown(
            '<div class="section-title">2 · Notícia carregada</div>',
            unsafe_allow_html=True,
        )

        link_html = (
            f' · <a href="{noticia["url"]}" target="_blank" rel="noopener noreferrer" '
            f'style="color:#2C5364">Original ↗</a>'
            if noticia.get("url")
            else ""
        )
        st.markdown(
            f'<div class="noticia-preview">'
            f'<div class="np-titulo">📰 {noticia.get("titulo", "Sem título")}</div>'
            f'<div class="np-fonte">Fonte: {noticia.get("fonte", "—")}{link_html}</div>'
            f'<div class="np-preview">{noticia.get("texto", "")[:400]}…</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        col_proc1, col_proc2, col_proc3 = st.columns([2, 2, 1])
        with col_proc1:
            btn_processar = st.button(
                "Rodar análise PLN", use_container_width=True, type="primary"
            )
        with col_proc2:
            btn_limpar = st.button("Descartar notícia", use_container_width=True)
        with col_proc3:
            st.caption(f"~{len(noticia.get('texto', '').split())} palavras")

        if btn_limpar:
            st.session_state["noticia_atual"] = None
            st.session_state["resultado"] = None
            st.session_state["resultados_busca"] = None
            st.rerun()

        if btn_processar:
            if not api_key:
                st.error("MARITACA_API_KEY ausente no .env.")
            else:
                try:
                    with st.status("Processando com PLN…", expanded=True) as status_box:
                        st.write("Preparando texto…")
                        st.write("Sentimento + resumo (Sabiá-4)…")
                        resultado = executar_analise_pln(
                            noticia,
                            api_key,
                            idioma_ui=idioma,
                            profundidade=profundidade,
                        )
                        st.write("Concluído.")
                        status_box.update(label="Pronto.", state="complete")

                    st.session_state["resultado"] = resultado

                    res = resultado["resumo"]
                    # Evita duplicatas exatas usando o resumo para que textos diferentes sem título (aba Texto) entrem no histórico.
                    if res not in [h.get("resumo_completo", "") for h in st.session_state.historico]:
                        st.session_state.historico.append(
                            {
                                "titulo": resultado["titulo"],
                                "fonte": resultado["fonte"],
                                "sentimento": resultado["sentimento"],
                                "confianca": resultado["confianca"],
                                "score": resultado.get("score_sentimento", ""),
                                "resumo": res[:180] + "..." if len(res) > 180 else res,
                                "resumo_completo": res,
                                "topicos": ", ".join(resultado.get("topicos", [])),
                                "palavras_chave": ", ".join(resultado.get("palavras_chave", [])),
                            }
                        )
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ {e}")
                except RuntimeError as e:
                    st.error(f"❌ API: {e}")
                except Exception as e:
                    st.error(f"❌ {e}")

    if st.session_state.get("resultado"):
        st.markdown("---")
        st.markdown(
            '<div class="section-title">3 · Resultado</div>',
            unsafe_allow_html=True,
        )
        renderizar_resultado(st.session_state["resultado"])

        st.markdown("<br>", unsafe_allow_html=True)
        r = st.session_state["resultado"]
        col_a1, col_a2, col_a3 = st.columns(3)

        with col_a1:
            txt = (
                f"NEWSANALYZER — RESULTADO\n{'='*40}\n\n"
                f"TÍTULO: {r['titulo']}\nFONTE: {r['fonte']}\nURL: {r.get('url', 'N/A')}\n\n"
                f"SENTIMENTO: {r['sentimento']} ({r.get('confianca', '')})\n"
                f"SCORE: {r.get('score_sentimento', '')}/100\n"
                f"JUSTIFICATIVA: {r.get('justificativa', '')}\n\n"
                f"RESUMO:\n{r['resumo']}\n\n"
                f"PALAVRAS-CHAVE: {', '.join(r.get('palavras_chave', []))}\n"
                f"TÓPICOS: {', '.join(r.get('topicos', []))}\n\n"
                f"TEXTO ORIGINAL:\n{r['texto_original']}\n"
            )
            st.download_button(
                "Exportar .txt",
                data=txt.encode("utf-8"),
                file_name="analise_noticia.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_a2:
            st.download_button(
                "Exportar .json",
                data=json.dumps(
                    {k: v for k, v in r.items() if k != "texto_limpo"},
                    ensure_ascii=False,
                    indent=2,
                ).encode("utf-8"),
                file_name="analise_noticia.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_a3:
            if st.button("Nova análise", use_container_width=True):
                st.session_state["resultado"] = None
                st.session_state["noticia_atual"] = None
                st.session_state["resultados_busca"] = None
                st.rerun()

    elif not noticia:
        st.markdown(
            """
        <div class="welcome-box">
          <div class="wb-icon">🚀</div>
          <h3>Comece por uma URL, texto ou busca</h3>
          <p>Use as abas acima para carregar uma notícia e depois rodar o PLN.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        cols = st.columns(3)
        cards = [
            ("🔗", "URL", "Extração automática do artigo."),
            ("🧠", "Sentimento", "Classe + score + justificativa."),
            ("📝", "Resumo", "Resumo + palavras-chave + tópicos."),
        ]
        for col, (icon, title, desc) in zip(cols, cards):
            with col:
                st.markdown(
                    f'<div class="feature-card">'
                    f'<div class="fc-icon">{icon}</div>'
                    f'<strong class="fc-title">{title}</strong>'
                    f'<p class="fc-desc">{desc}</p>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

        st.markdown(
            """
        <div class="tech-footer">
          Python · Streamlit · Sabiá-4 · BeautifulSoup · newspaper3k
        </div>
        """,
            unsafe_allow_html=True,
        )

    _renderizar_historico()


def _renderizar_historico():
    historico = st.session_state.get("historico", [])
    if not historico:
        return

    st.markdown("---")
    st.markdown("#### Histórico da Sessão")

    df = pd.DataFrame(historico)
    contagem = df["sentimento"].value_counts()

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Total de Análises", len(df))
    with col_s2:
        st.metric("Positivas 🟢", int(contagem.get("Positivo", 0)))
    with col_s3:
        st.metric("Negativas 🔴", int(contagem.get("Negativo", 0)))
    with col_s4:
        st.metric("Neutras 🟡", int(contagem.get("Neutro", 0)))

    st.markdown("<br>", unsafe_allow_html=True)

    if len(df) > 0:
        filtro = st.multiselect(
            "⏬ Explorar histórico (filtre por sentimento):",
            options=["Positivo", "Negativo", "Neutro"],
            default=["Positivo", "Negativo", "Neutro"],
        )
        df_f = df[df["sentimento"].isin(filtro)] if filtro else df
        
        for _, row in df_f.iterrows():
            emoji = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "🟡"}.get(row["sentimento"], "⚪")
            cor = {"Positivo": "#22c55e", "Negativo": "#ef4444", "Neutro": "#eab308"}.get(row["sentimento"], "gray")
            
            card_html = f"""<div style="background-color: var(--secondary-background-color); border-left: 4px solid {cor}; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); font-family: 'DM Sans', sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; gap: 16px; flex-wrap: wrap;">
<div style="flex: 1; min-width: 200px;">
<h3 style="color: var(--text-color); margin: 0 0 4px 0; font-size: 18px; font-weight: 700; line-height: 1.3;">{html.escape(str(row['titulo']))}</h3>
<div style="color: var(--text-color); opacity: 0.6; font-size: 12px; font-weight: 600;">FONTE: {html.escape(str(row['fonte']))}</div>
</div>
<div style="background-color: var(--background-color); border: 1px solid rgba(128,128,128,0.1); padding: 8px 14px; border-radius: 8px; text-align: center; min-width: 130px;">
<div style="font-size: 14px; font-weight: 700; color: var(--text-color);">{emoji} {html.escape(str(row['sentimento']))}</div>
<div style="font-size: 11px; color: var(--text-color); opacity: 0.6; margin-top: 2px;">CONFIANÇA: {html.escape(str(row['confianca']))}</div>
</div>
</div>
<div style="color: var(--text-color); opacity: 0.85; font-size: 14px; line-height: 1.6; border-top: 1px solid rgba(128,128,128,0.1); padding-top: 12px;">{html.escape(str(row['resumo']))}</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.download_button(
            "Exportar Histórico (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="historico_newsanalyzer.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e2:
        st.download_button(
            "Exportar Histórico (JSON)",
            data=json.dumps(historico, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="historico_newsanalyzer.json",
            mime="application/json",
            use_container_width=True,
        )
