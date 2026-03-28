"""
components/result_card.py — Saída da análise na ordem pedida:
1) Notícia extraída · 2) Sentimento (+ score) · 3) Resumo · extras (palavras-chave / tópicos)
"""

import html
import streamlit as st

def renderizar_resultado(resultado: dict):
    """Renderiza a análise com interface profissional e polida, omitindo o texto completo."""

    titulo = html.escape(str(resultado.get("titulo", "Sem título")))
    sentimento = html.escape(str(resultado.get("sentimento", "Neutro")))
    confianca = html.escape(str(resultado.get("confianca", "")))
    justificativa = html.escape(str(resultado.get("justificativa", "")))
    resumo = html.escape(str(resultado.get("resumo", "")))
    fonte = html.escape(str(resultado.get("fonte", "Desconhecida")))
    url = resultado.get("url")
    
    emoji = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "🟡"}.get(sentimento, "⚪")
    cor_borda = {"Positivo": "#22c55e", "Negativo": "#ef4444", "Neutro": "#eab308"}.get(sentimento, "gray")
    
    link_html = f' &bull; <a href="{html.escape(str(url))}" target="_blank" style="color: var(--primary-color); text-decoration: none; font-weight: 600;">Ver original ↗</a>' if url else ""

    html_content = f"""<div style="background-color: var(--secondary-background-color); border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 24px; border-top: 5px solid {cor_borda}; font-family: 'DM Sans', sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; flex-wrap: wrap; gap: 20px;">
<div style="flex: 1; min-width: 250px;">
<p style="text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: var(--text-color); opacity: 0.6; margin: 0 0 8px 0; font-weight: 700;">Notícia Analisada</p>
<h2 style="color: var(--text-color); margin: 0 0 8px 0; font-size: 24px; font-weight: 800; line-height: 1.3;">{titulo}</h2>
<div style="font-size: 14px; color: var(--text-color); opacity: 0.7;"><strong>{fonte}</strong> {link_html}</div>
</div>
<div style="text-align: right; background: var(--background-color); padding: 14px 20px; border-radius: 12px; border: 1px solid rgba(128,128,128,0.1); min-width: 160px;">
<div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-color); opacity: 0.6; font-weight: 700; margin-bottom: 4px;">Sentimento</div>
<div style="font-size: 22px; font-weight: 800; color: var(--text-color);">{emoji} {sentimento}</div>
<div style="font-size: 12px; color: var(--text-color); opacity: 0.7; margin-top: 4px;">Confiança: <strong>{confianca}</strong></div>
</div>
</div>
<div style="background-color: var(--background-color); border-radius: 12px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(128,128,128,0.1); border-left: 4px solid var(--primary-color);">
<p style="text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: var(--text-color); opacity: 0.6; margin: 0 0 12px 0; font-weight: 700;">Resumo Automático</p>
<div style="color: var(--text-color); font-size: 16px; line-height: 1.8;">{resumo}</div>
</div>"""

    if justificativa:
        html_content += f"""<div style="margin-bottom: 24px; padding: 16px 20px; background-color: rgba(128,128,128,0.05); border-radius: 10px;">
<p style="text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: var(--text-color); opacity: 0.6; margin: 0 0 8px 0; font-weight: 700;">Justificativa do Sentimento</p>
<div style="color: var(--text-color); font-size: 14px; line-height: 1.6; opacity: 0.9;">{justificativa}</div>
</div>"""

    palavras_chave = resultado.get("palavras_chave", [])
    topicos = resultado.get("topicos", [])
    
    if palavras_chave or topicos:
        html_content += '<div style="display: flex; gap: 24px; flex-wrap: wrap;">'
        if palavras_chave:
            tags = "".join([f'<span style="background-color: rgba(128,128,128,0.08); border: 1px solid rgba(128,128,128,0.2); color: var(--text-color); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; white-space: nowrap; display: inline-block; margin-right: 6px; margin-bottom: 6px;">{html.escape(str(p))}</span>' for p in palavras_chave if p])
            html_content += f"""<div style="flex: 1; min-width: 250px;">
<p style="text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: var(--text-color); opacity: 0.6; margin: 0 0 12px 0; font-weight: 700;">Palavras-Chave</p>
<div style="display: flex; flex-wrap: wrap;">{tags}</div>
</div>"""
            
        if topicos:
            tags = "".join([f'<span style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.3); color: var(--text-color); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; white-space: nowrap; display: inline-block; margin-right: 6px; margin-bottom: 6px;">{html.escape(str(t))}</span>' for t in topicos if t])
            html_content += f"""<div style="flex: 1; min-width: 250px;">
<p style="text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: var(--text-color); opacity: 0.6; margin: 0 0 12px 0; font-weight: 700;">Tópicos Mapeados</p>
<div style="display: flex; flex-wrap: wrap;">{tags}</div>
</div>"""
        html_content += '</div>'

    html_content += "</div>"
    
    st.markdown(html_content, unsafe_allow_html=True)
