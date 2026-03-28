"""
utils/text_cleaner.py — Utilitários de limpeza e preparação de texto

Responsabilidades:
  - Limpeza de texto bruto (remoção de ruído, normalização)
  - Extração automática de título quando não fornecido
  - Validação básica de conteúdo
"""

import re
import unicodedata


def limpar_texto(texto: str) -> str:
    """
    Limpa e normaliza o texto de uma notícia para processamento PLN.

    Operações realizadas:
      1. Remove URLs
      2. Remove referências a imagens, vídeos e legendas
      3. Normaliza espaços em branco e quebras de linha
      4. Remove caracteres de controle
      5. Remove linhas muito curtas (menus, labels, etc.)

    Args:
        texto: Texto bruto extraído da notícia

    Returns:
        Texto limpo e normalizado
    """
    if not isinstance(texto, str):
        return ""

    # Remove URLs
    texto = re.sub(r"https?://\S+", " ", texto)
    texto = re.sub(r"www\.\S+", " ", texto)

    # Remove e-mails
    texto = re.sub(r"\S+@\S+\.\S+", " ", texto)

    # Remove hashtags e menções
    texto = re.sub(r"[@#]\w+", " ", texto)

    # Remove emojis e caracteres especiais não-latinos
    texto = re.sub(r"[^\x00-\x7FÀ-ÿ\u0100-\u024F\s.,;:!?\"'()\-–—\[\]{}]", " ", texto)

    # Remove padrões comuns de navegação/UI de sites
    padroes_remover = [
        r"Leia (também|mais|a seguir)[\s\S]{0,100}?\.",
        r"Compartilhe (este|essa|o) (artigo|notícia|conteúdo)",
        r"Siga[-\s]nos (no|em|no)\s+\w+",
        r"©\s*\d{4}",
        r"Todos os direitos reservados",
        r"Publicidade",
        r"PUBLICIDADE",
        r"Anúncio",
        r"Newsletter",
        r"\[[\w\s]+\]",  # Remove [tags] residuais
    ]
    for padrao in padroes_remover:
        texto = re.sub(padrao, " ", texto, flags=re.IGNORECASE)

    # Normaliza espaços e quebras de linha
    texto = re.sub(r"\t", " ", texto)
    texto = re.sub(r"\r\n|\r|\n", " ", texto)
    texto = re.sub(r" {2,}", " ", texto)

    # Remove linhas/segmentos muito curtos (prováveis fragmentos de UI)
    segmentos = [s.strip() for s in texto.split(".") if len(s.strip().split()) >= 4]
    texto = ". ".join(segmentos)

    # Trim final
    texto = texto.strip()

    return texto


def extrair_titulo(texto: str) -> str:
    """
    Extrai automaticamente um possível título a partir do início do texto.
    Usa a primeira frase com mais de 5 palavras como título.

    Args:
        texto: Texto da notícia

    Returns:
        String com o título extraído ou "Notícia sem título"
    """
    if not texto:
        return "Notícia sem título"

    # Tenta a primeira linha
    primeira_linha = texto.split("\n")[0].strip()
    if 5 <= len(primeira_linha.split()) <= 25:
        return primeira_linha

    # Tenta a primeira frase
    match = re.match(r"([^.!?]{20,120}[.!?])", texto.strip())
    if match:
        return match.group(1).strip()

    # Fallback: primeiras 10 palavras
    palavras = texto.split()[:10]
    if palavras:
        return " ".join(palavras) + "..."

    return "Notícia sem título"


def contar_palavras(texto: str) -> int:
    """Conta o número de palavras em um texto."""
    if not texto:
        return 0
    return len(texto.split())


def validar_texto(texto: str, min_palavras: int = 20) -> tuple[bool, str]:
    """
    Valida se um texto tem conteúdo suficiente para análise.

    Returns:
        (valido, mensagem_erro)
    """
    if not texto or not texto.strip():
        return False, "Texto vazio."

    n_palavras = contar_palavras(texto)
    if n_palavras < min_palavras:
        return False, f"Texto muito curto: {n_palavras} palavras (mínimo: {min_palavras})."

    return True, ""
