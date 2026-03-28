# 📰 NewsAnalyzer

<div align="center">
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.32.0%2B-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</div>

<br>

**NewsAnalyzer** é uma aplicação web interativa desenvolvida em Python com a interface do Streamlit. O projeto foca em **Análise de Conteúdo Jornalístico** utilizando Processamento de Linguagem Natural (PLN) de forma automatizada.

---

## 👥 Equipe (FIAP)

| Nome                                | RM       |
| ----------------------------------- | -------- |
| Sofia Bueris Netto de Souza         | RM565818 |
| Vinícius Adrian Siqueira de Oliveira| RM564962 |
| Augusto Oliveira Codo de Sousa      | RM562080 |
| Felipe de Oliveira Cabral           | RM561720 |
| Gabriel Tonelli Avelino Dos Santos  | RM564705 |

---

## 💡 Sobre o Projeto

O **NewsAnalyzer** permite a extração e análise automatizadas de notícias jornalísticas, entregando dois processamentos principais baseados no modelo de linguagem **Sabiá-4** da **Maritaca AI**:
1. **Análise de Sentimento:** Classificação do viés emocional do texto, incluindo percentual de confiança e uma justificativa lógica baseada na matéria.
2. **Geração de Resumo:** Resumo automático listando os pontos-chave, categorias pertinentes e palavras-chave principais.

### 📥 Formas de Entrada Suportadas

- **🌎 Extração por URL:** O sistema obtém e processa o conteúdo principal do artigo através da URL informada.
- **✏️ Texto Manual:** O usuário pode colar diretamente na plataforma o teor integral para ser analisado.
- **🔍 Busca por Tema:** Uma integração via RSS rastreia as notícias mais recentes sobre uma palavra-chave para análise imediata do fluxo narrativo do tema fornecido.

Os resultados processados são dispostos em "cards" visuais interativos e organizados, permitindo também a exportação ágil em formatos `.txt` ou `.json`.

---

## 🏗️ Arquitetura do Sistema

O projeto adota uma arquitetura estruturada, separando componentes em camadas de responsabilidade bem delimitadas garantindo que a interface principal separe-se do processamento lógico e negocial.

```text
NewsAnalyzer/
│
├── app.py                    # Entrypoint (Streamlit), definições base e roteamento
│
├── views/                    # Camada de Apresentação (Páginas)
│   ├── analyzer.py           # Interface operacional de análise (Aba de PLN)
│   └── home.py               # Landing page e contextualizações
│
├── pipeline/                 
│   └── news_pipeline.py      # Orquestração do fluxo de processamentos de análise de textos
│
├── providers/                
│   └── maritaca_pln.py       # Ponto de Integração (Requests/API) com a Maritaca AI
│
├── services/                 # Regras de Negócio e Dados
│   └── news_fetcher.py       # Módulo para raspagem e coleta da internet
│
├── components/               # Elementos React-like (Widgets Visuais Interativos)
│   ├── result_card.py        # Módulo encarregado da renderização do display das análises
│   └── styles.py             # Estilização CSS personalizada injetada no Streamlit
│
├── utils/                    
│   └── text_cleaner.py       # Serviços auxiliares de sanitização, normalização e parsing
│
├── .env                      # Variáveis de ambiente secretas (Não versionado)
├── .gitignore                # Regras de arquivos não rastreados
├── requirements.txt          # Dependências mapeadas necessárias para instanciar o backend
└── LICENSE                   # Licença aplicável ao pacote (MIT)
```

### 🔄 Fluxo de Processamento

1. **Entrada de Dados:** (`news_fetcher.py`) → Faz a busca web e converte a URL/Tema em puro texto.
2. **Sanitização:** (`text_cleaner.py`) → O texto bruto é limpo, formatado das impuras marcações e padronizado.
3. **Delegação PLN:** (`news_pipeline.py` → `maritaca_pln.py`) → O conteúdo limpo é encaminhado via interface ao end-point da API Sabiá-4.
4. **Respostas e UI:** (`views/` e `result_card.py`) → O sistema processa positivamente as respostas recebidas em elementos visuais limpos.

---

## 🛠️ Tecnologias e Bibliotecas

| Tecnologia | Versão Mínima | Descrição / Função |
| :--- | :--- | :--- |
| **Python** | `3.10+` | Linguagem base do projeto backend/frontend. |
| **Streamlit** | `1.32.0` | Framework web single-page (SPA). |
| **Sabiá-4** | *(Maritaca AI)* | Modelo de Linguagem Grande (LLM) encarregado da compreensão contextual. |
| **requests** | `2.31.0` | Realiza as requisições HTTP REST aos providers externos e Feedbacks RSS. |
| **BeautifulSoup4** | `4.12.0` | Utilizada como ferramenta de extração alternativa e parsing para o HTML corrompido. |
| **newspaper3k** | `0.2.8` | Biblioteca encarregada de destilar reportagens extensas mantendo a relevância central. |
| **lxml** | `5.0.0` | Parser de alto desempenho operando em conjunto com o BeautifulSoup. |

> **Nota Integrativa:** Toda e qualquer inteligência de análise semântica emana da infraestrutura externa da Maritaca AI. A aplicação modela as prompts adequadas dentro das restrições e envia para processamento — não se valendo de inferências dispendiosas locais. 

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python na versão `>= 3.10`
- Configuração de uma Cloud API Key adquirida junto ao serviço [Maritaca AI](https://maritaca.ai).

### Instalação

**1. Clone o projeto e acesse as pastas:**
```bash
git clone https://github.com/Sofiabns/NewsAnalyzer.git
cd NewsAnalyzer
```

**2. Crie e ative um ambiente virtual (`venv`):**
  - *No Windows:*
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
  - *No Linux/macOS:*
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

**3. Instale as dependências listadas no projeto:**
```bash
pip install -r requirements.txt
```
*(Nota: dependendo de seu sistema operacional, a biblioteca C-based `lxml` pode requerer `pip install lxml --force-reinstall` para compilação adequada).*

**4. Aja com Variáveis de Ambiente:**
Crie o arquivo protegido de contexto em `.env` na raiz do seu projeto. Insira sua chave respectiva de acesso da Maritaca AI:
```env
MARITACA_API_KEY=sua_chave_de_api_aqui
```

**5. Inicialize o App:**
```bash
streamlit run app.py
```
A plataforma estará acessível no navegador através do endereço genérico: `http://localhost:8501`.

---

## ⚠️ Limitações Conhecidas

- **Single Page Applications (SPAs) & Paywalls:**  
  Plataformas jornalísticas mais modernas que confiam intensamente no JavaScript para montagem atrasada do DOM (Revisões client-side) ou limitadas por muros de pagamento (paywall) podem ser opacas ao módulo `newspaper3k`. Nestes casos a busca colapsa; nestes canais recomenda-se a inserção pelo campo "Texto Manual".
  
- **Escopo e Integridade de RSS (Busca Livre por Tema):**  
  As pesquisas via tema focam no Google News Feed (RSS), retornando resumos introdutórios e leads parciais geradas pela Indexação do Google — e não a substância total da matéria.

- **Threshold da API Sabiá-4:**  
  Para garantir que a performance permaneça ideal e restrições de processamento natural sejam mantidas, os longos ensaios são limitados com caracteres padronizados antes do envio às matrizes de predição (comentado internamente à ~2.000 para sentimentos e 3.000 tokens aproximados para sínteses). 

- **Persistência Temporária de Sessões Streamlit:**  
  O histórico operado na barra lateral direita é preservado temporariamente na sessão local (`st.session_state`). Dar refresh generalista no browser fará com que essa alocação pereça. Aconselha-se utilizar as opções integradas de "Exportar JSON/TXT" do programa em avaliações primordiais.

---

<div align="center">
  <small>Desenvolvido para fins práticos em PLN como objeto do projeto de avaliação (FIAP). Licenciado ao abrigo da Open Source MIT License.</small>
</div>
