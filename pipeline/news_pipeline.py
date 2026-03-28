"""
pipeline/news_pipeline.py — Pipeline de análise

Encadeia limpeza de texto e chamadas ao provider (Sabiá-4), produzindo um único dict
consumido pela interface. Separa a UI da lógica de negócio e do provider.
"""

from utils.text_cleaner import limpar_texto
from providers.maritaca_pln import analisar_sentimento, gerar_resumo


def executar_analise_pln(
    noticia: dict,
    api_key: str,
    idioma_ui: str,
    profundidade: str,
) -> dict:
    """
    Executa o fluxo completo PLN sobre uma notícia já coletada (título, texto, fonte, url).

    Args:
        noticia: dict com pelo menos 'titulo', 'texto', 'fonte'; 'url' opcional.
        api_key: MARITACA_API_KEY
        idioma_ui: valor do select na UI ('Automático', 'Português', ...)
        profundidade: 'Breve' | 'Padrão' | 'Detalhado'

    Returns:
        Dict pronto para session_state['resultado'] e para os componentes de UI.

    Raises:
        ValueError: texto insuficiente após limpeza.
        RuntimeError: repassa erros críticos do provider (ex.: API).
    """
    texto_bruto = noticia.get("texto") or ""
    texto_limpo = limpar_texto(texto_bruto)
    if len(texto_limpo.split()) < 15:
        raise ValueError("Texto muito curto para análise (mínimo ~15 palavras após limpeza).")

    idioma = idioma_ui if idioma_ui != "Automático" else None

    sentimento_r = analisar_sentimento(texto_limpo, api_key, idioma=idioma)
    resumo_r = gerar_resumo(texto_limpo, api_key, profundidade=profundidade, idioma=idioma)

    return {
        "titulo": noticia.get("titulo", "Sem título"),
        "texto_original": texto_bruto,
        "texto_limpo": texto_limpo,
        "fonte": noticia.get("fonte", "Desconhecida"),
        "url": noticia.get("url"),
        "sentimento": sentimento_r.get("classificacao", "Neutro"),
        "confianca": sentimento_r.get("confianca", ""),
        "justificativa": sentimento_r.get("justificativa", ""),
        "score_sentimento": sentimento_r.get("score", 50),
        "resumo": resumo_r.get("resumo", ""),
        "palavras_chave": resumo_r.get("palavras_chave", []),
        "topicos": resumo_r.get("topicos", []),
    }
