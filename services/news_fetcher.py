"""
services/news_fetcher.py — Módulo de coleta de notícias

Responsabilidades:
  - Etapa 1A: Buscar e extrair conteúdo de uma URL de notícia
  - Etapa 1B: Buscar notícias por tema via Google News RSS
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
import xml.etree.ElementTree as ET


# ─────────────────────────────────────────────────────────────────────────────
#  HEADERS HTTP
# ─────────────────────────────────────────────────────────────────────────────

HEADERS_WEB = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

HEADERS_RSS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "pt-BR,pt;q=0.9",
}


# ─────────────────────────────────────────────────────────────────────────────
#  ETAPA 1A — BUSCA POR URL
# ─────────────────────────────────────────────────────────────────────────────

def buscar_por_url(url: str) -> dict:
    resultado = _extrair_com_newspaper(url)
    if resultado and not resultado.get("erro"):
        return resultado
    return _extrair_com_bs4(url)


def _extrair_com_newspaper(url: str) -> dict:
    try:
        from newspaper import Article
        artigo = Article(url, language="pt")
        artigo.download()
        artigo.parse()
        texto = artigo.text.strip()
        titulo = artigo.title.strip() if artigo.title else ""
        if not texto or len(texto.split()) < 20:
            return {"erro": "Conteúdo insuficiente extraído com newspaper3k."}
        return {
            "titulo": titulo or _extrair_dominio(url),
            "texto": texto,
            "fonte": _extrair_dominio(url),
            "url": url,
            "data": artigo.publish_date.strftime("%Y-%m-%d") if artigo.publish_date else "",
        }
    except ImportError:
        return {"erro": "newspaper3k não disponível."}
    except Exception as e:
        return {"erro": f"newspaper3k: {str(e)[:80]}"}


def _extrair_com_bs4(url: str) -> dict:
    try:
        resp = requests.get(url, headers=HEADERS_WEB, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer",
                         "aside", "advertisement", "iframe", "noscript",
                         "figure", "figcaption"]):
            tag.decompose()
        titulo = ""
        for sel in ["h1", "title", 'meta[property="og:title"]']:
            el = soup.select_one(sel)
            if el:
                titulo = el.get("content", "") or el.get_text(strip=True)
                if titulo:
                    break
        seletores = [
            "article", '[class*="article-body"]', '[class*="article-content"]',
            '[class*="post-content"]', '[class*="news-body"]', '[class*="materia"]',
            '[class*="conteudo"]', '[class*="content-body"]', '[itemprop="articleBody"]',
            "main", '[role="main"]',
        ]
        texto = ""
        for sel in seletores:
            el = soup.select_one(sel)
            if el:
                parags = el.find_all(["p", "h2", "h3"])
                texto = " ".join(p.get_text(separator=" ", strip=True)
                                 for p in parags if len(p.get_text(strip=True)) > 30)
                if len(texto.split()) > 50:
                    break
        if len(texto.split()) < 50:
            parags = soup.find_all("p")
            texto = " ".join(
                p.get_text(separator=" ", strip=True)
                for p in parags if len(p.get_text(strip=True)) > 40
            )
        if len(texto.split()) < 20:
            return {"erro": "Não foi possível extrair texto. Tente colar o texto manualmente."}
        return {
            "titulo": titulo or _extrair_dominio(url),
            "texto": texto[:8000],
            "fonte": _extrair_dominio(url),
            "url": url,
            "data": "",
        }
    except requests.exceptions.ConnectionError:
        return {"erro": "Não foi possível conectar ao endereço. Verifique a URL."}
    except requests.exceptions.Timeout:
        return {"erro": "Timeout ao acessar a URL."}
    except requests.exceptions.HTTPError as e:
        return {"erro": f"Erro HTTP {e.response.status_code}."}
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)[:100]}"}


def _extrair_dominio(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return "Portal de notícias"


# ─────────────────────────────────────────────────────────────────────────────
#  ETAPA 1C — BUSCA POR TEMA (Google News RSS)
# ─────────────────────────────────────────────────────────────────────────────

def buscar_por_tema(query: str, idioma: str = "pt-BR", max_resultados: int = 5) -> list:
    """
    Busca notícias via Google News RSS.
    Usa xml.etree.ElementTree diretamente para evitar problemas com parsers do BS4.
    """
    lang_map = {
        "pt-BR": ("pt-BR", "BR", "BR:pt"),
        "en-US": ("en-US", "US", "US:en"),
        "es-419": ("es-419", "MX", "MX:es-419"),
    }
    hl, gl, ceid = lang_map.get(idioma, ("pt-BR", "BR", "BR:pt"))

    url = (
        f"https://news.google.com/rss/search"
        f"?q={quote_plus(query)}&hl={hl}&gl={gl}&ceid={ceid}"
    )

    try:
        resp = requests.get(url, headers=HEADERS_RSS, timeout=20)
        resp.raise_for_status()

        # ── Parse com ElementTree (mais confiável que BS4 para XML RSS) ──
        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError:
            # Se o XML vier malformado, tenta limpar e reprocessar
            texto_limpo = resp.text.encode("utf-8", errors="replace")
            root = ET.fromstring(texto_limpo)

        # Namespace do Google News (às vezes presente)
        ns = {"media": "http://search.yahoo.com/mrss/"}

        items = root.findall(".//item")

        noticias = []
        for item in items[:max_resultados]:
            # ── Título ──
            titulo_el = item.find("title")
            titulo = titulo_el.text.strip() if titulo_el is not None and titulo_el.text else ""

            # Remove sufixo "- Fonte" que o Google News adiciona
            if " - " in titulo:
                titulo = titulo.rsplit(" - ", 1)[0].strip()

            # ── Link (URL da notícia) ──
            # No RSS do Google News, <link> é um texto simples entre tags
            # ElementTree armazena o texto após uma tag como .tail do elemento anterior
            link = ""
            link_el = item.find("link")
            if link_el is not None:
                # .tail contém o texto DEPOIS da tag de fechamento no XML
                if link_el.tail and link_el.tail.strip().startswith("http"):
                    link = link_el.tail.strip()
                elif link_el.text and link_el.text.strip().startswith("http"):
                    link = link_el.text.strip()

            # Fallback: <guid> geralmente contém a URL
            if not link:
                guid_el = item.find("guid")
                if guid_el is not None and guid_el.text:
                    candidate = guid_el.text.strip()
                    if candidate.startswith("http"):
                        link = candidate

            # ── Descrição / resumo ──
            desc_el = item.find("description")
            resumo = ""
            if desc_el is not None and desc_el.text:
                # A descrição do Google News é HTML com links — limpa com BS4
                inner = BeautifulSoup(desc_el.text, "html.parser")
                resumo = inner.get_text(separator=" ", strip=True)
                resumo = re.sub(r"\s+", " ", resumo).strip()[:500]

            # ── Data ──
            pub_el = item.find("pubDate")
            data_str = ""
            if pub_el is not None and pub_el.text:
                try:
                    from email.utils import parsedate_to_datetime
                    data_str = parsedate_to_datetime(pub_el.text.strip()).strftime("%d/%m/%Y")
                except Exception:
                    data_str = pub_el.text.strip()[:10]

            # ── Fonte ──
            src_el = item.find("source")
            fonte = src_el.text.strip() if src_el is not None and src_el.text else "Google News"

            # Texto combinado
            texto = f"{titulo}. {resumo}" if resumo else titulo

            if len(titulo) > 5:
                noticias.append({
                    "titulo": titulo,
                    "texto": texto,
                    "fonte": fonte,
                    "url": link,
                    "data": data_str,
                })

        return noticias

    except Exception as e:
        print(f"[news_fetcher] Erro na busca por tema: {type(e).__name__}: {e}")
        return []
