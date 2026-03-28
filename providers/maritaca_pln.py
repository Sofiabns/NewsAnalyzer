"""
providers/maritaca_pln.py — Provider PLN (CP1 adaptado à interface)

Integra o modelo Sabiá-4 (Maritaca AI): sentimento estruturado + resumo da notícia.
A interface e o pipeline consomem apenas os dicionários retornados por estas funções.
"""

import json
from typing import Optional

import requests

# ─────────────────────────────────────────────────────────────────────────────
#  API MARITACA (SABIÁ-4)
# ─────────────────────────────────────────────────────────────────────────────

MARITACA_URL = "https://chat.maritaca.ai/api/chat/completions"
# Nome canônico na API Maritaca (docs: sabia-4; aceita também variantes com acento)
MARITACA_MODEL = "sabia-4"


def _call_sabia(
    messages: list,
    api_key: str,
    max_tokens: int = 600,
    temperature: float = 0.2,
) -> str:
    """Chamada base ao Sabiá-4. Retorna o texto da mensagem ou levanta RuntimeError."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": MARITACA_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        resp = requests.post(MARITACA_URL, headers=headers, json=payload, timeout=45)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.Timeout:
        raise RuntimeError("Timeout na comunicação com o Sabiá-4. Tente novamente.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Erro HTTP na API Sabiá-4: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro ao comunicar com Sabiá-4: {e}")


def _strip_json_fences(raw: str) -> str:
    s = raw.strip()
    if "```" in s:
        parts = s.split("```")
        if len(parts) >= 2:
            s = parts[1]
            if s.startswith("json"):
                s = s[4:]
    return s.strip()


# ─────────────────────────────────────────────────────────────────────────────
#  ANÁLISE DE SENTIMENTO
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_SENTIMENTO = """Você é um especialista em PLN focado em conteúdo jornalístico.

Analise o sentimento da notícia e responda APENAS com um JSON válido:

{
  "classificacao": "Positivo" | "Negativo" | "Neutro",
  "confianca": "Alta" | "Média" | "Baixa",
  "justificativa": "2 a 3 frases objetivas explicando a classificação com base no texto.",
  "score": <número inteiro de 0 a 100: 0 muito negativo, 50 neutro, 100 muito positivo>
}

Critérios:
- Positivo: conquistas, avanços, resultados favoráveis, crescimento, soluções.
- Negativo: crises, conflitos, tragédias, denúncias graves, fracassos.
- Neutro: informação factual equilibrada, sem carga emocional predominante.

O campo "score" deve ser coerente com "classificacao" (ex.: Negativo costuma ficar abaixo de 40, Positivo acima de 60).

Responda só o JSON, sem markdown nem texto extra."""


def _score_padrao_por_classe(classificacao: str) -> int:
    return {"Positivo": 72, "Negativo": 28, "Neutro": 50}.get(classificacao, 50)


def analisar_sentimento(texto: str, api_key: str, idioma: Optional[str] = None) -> dict:
    """
    Retorna: classificacao, confianca, justificativa, score (0–100).
    """
    texto_truncado = texto[:2000]
    instrucao_idioma = f"\nO texto está em {idioma}." if idioma else ""
    mensagens = [
        {"role": "system", "content": SYSTEM_SENTIMENTO},
        {
            "role": "user",
            "content": (
                f"Analise o sentimento desta notícia:{instrucao_idioma}\n\n"
                f"NOTÍCIA:\n{texto_truncado}\n\n"
                f"Retorne apenas o JSON com classificacao, confianca, justificativa e score."
            ),
        },
    ]

    resposta = ""
    try:
        resposta = _call_sabia(mensagens, api_key, max_tokens=380, temperature=0.1)
        limpa = _strip_json_fences(resposta)
        resultado = json.loads(limpa)

        classificacao = resultado.get("classificacao", "Neutro")
        if classificacao not in ("Positivo", "Negativo", "Neutro"):
            classificacao = _fallback_sentimento(limpa)

        score = resultado.get("score")
        try:
            score = int(score)
            score = max(0, min(100, score))
        except (TypeError, ValueError):
            score = _score_padrao_por_classe(classificacao)

        return {
            "classificacao": classificacao,
            "confianca": resultado.get("confianca", "Média"),
            "justificativa": resultado.get("justificativa", ""),
            "score": score,
        }

    except json.JSONDecodeError:
        classificacao = _fallback_sentimento(resposta)
        return {
            "classificacao": classificacao,
            "confianca": "Baixa",
            "justificativa": "Não foi possível interpretar o JSON do modelo; classificação por heurística.",
            "score": _score_padrao_por_classe(classificacao),
        }
    except Exception as e:
        return {
            "classificacao": "Neutro",
            "confianca": "Baixa",
            "justificativa": f"Erro na análise: {str(e)[:200]}",
            "score": 50,
        }


def _fallback_sentimento(texto: str) -> str:
    t = (texto or "").lower()
    if "positivo" in t:
        return "Positivo"
    if "negativo" in t:
        return "Negativo"
    return "Neutro"


# ─────────────────────────────────────────────────────────────────────────────
#  RESUMO
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_RESUMO = """Você é um especialista em sumarização de notícias com PLN.

Analise a notícia e responda APENAS com JSON válido:

{
  "resumo": "Texto do resumo conforme a profundidade pedida.",
  "palavras_chave": ["...", "..."],
  "topicos": ["...", "..."]
}

- palavras_chave: 4 a 6 termos.
- topicos: 2 a 4 áreas temáticas (ex.: Política, Economia).

Responda só o JSON, sem markdown nem texto extra."""


PROFUNDIDADE_MAP = {
    "Breve": "Resumo BREVE: no máximo 2–3 frases com a informação principal.",
    "Padrão": "Resumo PADRÃO: um parágrafo de 4–6 frases com os pontos essenciais.",
    "Detalhado": (
        "Resumo DETALHADO: dois parágrafos com contexto, fatos, consequências e relevância."
    ),
}


def gerar_resumo(
    texto: str,
    api_key: str,
    profundidade: str = "Padrão",
    idioma: Optional[str] = None,
) -> dict:
    """Retorna: resumo, palavras_chave, topicos."""
    texto_truncado = texto[:3000]
    instrucao_prof = PROFUNDIDADE_MAP.get(profundidade, PROFUNDIDADE_MAP["Padrão"])
    if idioma:
        instrucao_idioma = f"\nO texto está em {idioma}. Responda em português."
    else:
        instrucao_idioma = "\nResponda em português."

    mensagens = [
        {"role": "system", "content": SYSTEM_RESUMO},
        {
            "role": "user",
            "content": (
                f"Gere o resumo estruturado.{instrucao_idioma}\n\n"
                f"Profundidade: {instrucao_prof}\n\n"
                f"NOTÍCIA:\n{texto_truncado}\n\n"
                f"Retorne apenas o JSON com resumo, palavras_chave e topicos."
            ),
        },
    ]

    resposta = ""
    try:
        resposta = _call_sabia(mensagens, api_key, max_tokens=650, temperature=0.3)
        limpa = _strip_json_fences(resposta)
        resultado = json.loads(limpa)

        palavras = resultado.get("palavras_chave", [])
        if isinstance(palavras, str):
            palavras = [p.strip() for p in palavras.split(",") if p.strip()]

        topicos = resultado.get("topicos", [])
        if isinstance(topicos, str):
            topicos = [t.strip() for t in topicos.split(",") if t.strip()]

        return {
            "resumo": resultado.get("resumo", "Resumo não disponível."),
            "palavras_chave": palavras[:6],
            "topicos": topicos[:4],
        }

    except json.JSONDecodeError:
        trecho = (resposta or "").strip()
        return {
            "resumo": trecho[:800] if trecho else "Não foi possível gerar o resumo estruturado.",
            "palavras_chave": [],
            "topicos": [],
        }
    except Exception as e:
        return {
            "resumo": f"Erro ao gerar resumo: {str(e)[:120]}",
            "palavras_chave": [],
            "topicos": [],
        }
