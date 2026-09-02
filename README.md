<h1 align="center">🏠 Indicium Price Predictor 🏠</h1>

<p align="center">
  <strong>Um modelo preditivo para prever preços de aluguéis temporários em Nova York! 🌆</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue" alt="Python Badge">
  <img src="https://img.shields.io/badge/Pandas-Latest-green" alt="Pandas Badge">
  <img src="https://img.shields.io/badge/Scikit-learn-1.6.1-orange" alt="Scikit-learn Badge">
  <img src="https://img.shields.io/badge/Flask-API-yellow" alt="Flask Badge">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Active Development Badge">
</p>

---

<h2 align="center">Do que se trata o Indicium Price Predictor?</h2>

<p align="center">
  O <strong>Indicium Price Predictor</strong> é um projeto desenvolvido para auxiliar na criação de uma plataforma de aluguéis temporários na cidade de Nova York. Ele utiliza técnicas de Ciência de Dados e Machine Learning para prever o preço ideal de aluguel com base em características como localização, tipo de quarto, disponibilidade e outros fatores relevantes. Além disso, o projeto inclui uma análise exploratória de dados (EDA) detalhada para entender as principais variáveis que impactam os preços.
</p>

---

<h2 align="center">🎯 Objetivos do Projeto 🎯</h2>

- **Análise Exploratória de Dados (EDA)**: Identificar padrões e insights nos dados fornecidos pelo cliente.
- **Modelagem Preditiva**: Desenvolver um modelo capaz de prever o preço de aluguel com base nas características do imóvel.
- **Validação do Modelo**: Avaliar a performance do modelo utilizando métricas como RMSE (Root Mean Squared Error).
- **API Flask**: Criar uma interface simples para prever preços a partir de novos dados inseridos pelo usuário.
---

<h2 align="center">🎮 Funcionalidades Principais 🎮</h2>

- **Análise Exploratória de Dados (EDA)**:
  - Visualização da distribuição de preços.
  - Análise de correlações entre variáveis numéricas.
  - Identificação de outliers e valores ausentes.
  - Insights sobre bairros com maior retorno financeiro.
- **Modelo Preditivo**:
  - Previsão de preços com base em características como localização, tipo de quarto e disponibilidade.
  - Uso de um pipeline de pré-processamento para tratar valores ausentes e codificar variáveis categóricas.
  - Treinamento e avaliação de um modelo de regressão (Random Forest Regressor).
- **Interface de Usuário**:
  - API Flask para receber entradas do usuário e retornar previsões.
  - Interface HTML simples para interação com o modelo.
---

<h2 align="center">🗂️ Estrutura do Projeto 🗂️</h2>

```plaintext
IncidiumCD/
├── app/
│   ├── app.py          # rotas Flask e o ponto de entrada (python app/app.py)
│   ├── config.py       # caminhos, colunas do modelo e variáveis de ambiente
│   ├── dataset.py      # carga do CSV e a busca por nome
│   ├── model.py        # carga do model.pkl.gz e o payload da previsão
│   ├── charts.py       # os onze gráficos da EDA, em base64 e com cache
│   ├── static/         # css e js da interface
│   └── templates/      # index.html (busca) e graph.html (gráficos)
├── data/
│   └── teste_indicium_precificacao.csv   # dataset original, ~49 mil linhas
├── notebooks/
│   ├── eda.ipynb                # análise exploratória
│   └── treinamento_modelo.py    # treina e gera o model.pkl.gz
├── tests/               # suíte pytest, sobe a aplicação com dados e modelo reais
├── model.pkl.gz         # modelo treinado, versionado no repositório
├── requirements.txt
└── requirements-dev.txt
```

Dentro de `app/` cada módulo cuida de uma coisa só: `config.py` não importa nada
dos outros módulos do projeto, `dataset.py` só entende de CSV, `model.py` só de
modelo, `charts.py` só de gráfico — e `app.py` apenas orquestra as rotas em cima
disso.

---

<h2 align="center">📦 Pacotes e Dependências Necessárias 📦</h2>

O projeto depende diretamente destes pacotes, nas versões em que foi testado:

```plaintext
Flask==3.1.3
pandas==3.0.5
numpy==2.5.2
scikit-learn==1.6.1
matplotlib==3.11.1
seaborn==0.13.2
```

São os mesmos do `requirements.txt` — as demais bibliotecas entram sozinhas, como
dependências dessas. Para rodar os testes, use o `requirements-dev.txt`.

A versão do **scikit-learn** é a que mais importa: o `model.pkl.gz` foi serializado
com ela, e abrir o pickle em outra versão pode falhar ou mudar o resultado sem avisar.

---

<h2 align="center">📚 Passo a Passo para Instalação 📚</h2>

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/RIGOandre/IncidiumCD.git
   ```

2. **Crie um Ambiente Virtual (Opcional, mas Recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   # lembre-se de permitir o uso de Scripts
      - Abra o PowerShell como administrador;
      - Então cole no terminal -> "Set-ExecutionPolicy RemoteSigned -Scope LocalMachine";
      - Em seguida digite S(Y) para concordar.
   ```

3. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a API Flask**:
   - O modelo treinado (`model.pkl.gz`) já vem no repositório, então não é
     preciso treinar nada para usar a aplicação.
     ```bash
     python app/app.py
     ```
   - Acesse a interface no navegador em `http://127.0.0.1:5000/`.
   - Porta, host, caminho do CSV... dá para mudar sem tocar no código, veja
     Variáveis de Ambiente logo abaixo.

5. **Teste o Modelo**:
   - Busque um anúncio pelo nome na interface e veja a previsão de preço.

6. **Retreine o Modelo (opcional)**:
   - Só é necessário se você trocar o CSV em `data/` ou quiser mexer no pipeline.
     ```bash
     python notebooks/treinamento_modelo.py
     ```
   - Os caminhos são resolvidos sozinhos a partir da pasta do projeto, não há
     nada para editar no script.
   - O treinamento leva de 5 a 10 minutos, dependendo da máquina, e sobrescreve
     o `model.pkl.gz`.

---

<h2 align="center">⚙️ Variáveis de Ambiente ⚙️</h2>

Nenhuma é obrigatória — sem elas a aplicação sobe com os padrões abaixo, os
mesmos usados nos testes. As três primeiras são lidas em `app/config.py`; as
outras quatro (log e as opções do `app.run()`) são lidas direto em `app/app.py`.

- **`INCIDIUM_CSV`**: caminho do CSV de anúncios. Padrão: `data/teste_indicium_precificacao.csv`, resolvido a partir da raiz do projeto (não do diretório de onde o comando é chamado).
- **`INCIDIUM_MODEL`**: caminho do arquivo do modelo (`.pkl` ou `.pkl.gz`). Sem ela, a aplicação procura, nessa ordem, `model.pkl.gz` e depois `model.pkl` na raiz do projeto.
- **`INCIDIUM_SEARCH_LIMIT`**: quantidade máxima de resultados que `/search` devolve. Padrão: `15`.
- **`INCIDIUM_LOG_LEVEL`**: nível de log (`DEBUG`, `INFO`, `WARNING`...). Padrão: `INFO`.
- **`INCIDIUM_HOST`**: endereço onde o Flask escuta. Padrão: `127.0.0.1`.
- **`INCIDIUM_PORT`**: porta onde o Flask escuta. Padrão: `5000`.
- **`INCIDIUM_DEBUG`**: liga o modo debug do Flask quando o valor é exatamente `"1"` (qualquer outro valor desliga). Padrão: `"1"` — ou seja, `python app/app.py` já sobe em modo debug.

Exemplo, mudando a porta e apontando para outro CSV:

```bash
# Windows (PowerShell)
$env:INCIDIUM_PORT = "8000"
$env:INCIDIUM_CSV = "C:\caminho\outro.csv"
python app/app.py

# Linux/macOS
INCIDIUM_PORT=8000 INCIDIUM_CSV=/caminho/outro.csv python app/app.py
```

---

<h2 align="center">🌐 Rotas Disponíveis 🌐</h2>

- **`GET /`**: tela de busca.
- **`GET /graph`**: página com os onze gráficos da EDA, que busca as imagens em `/generate_charts` via `fetch`.
- **`GET /search?q=termo`**: busca anúncios pelo nome (contém, sem diferenciar maiúsculas/minúsculas) e devolve até `INCIDIUM_SEARCH_LIMIT` resultados em JSON.
- **`POST /predict`**: recebe o JSON de um anúncio (o mesmo registro que `/search` devolve) e responde com o preço previsto. Corpo que não é JSON, ou que falta `latitude`, `longitude`, `bairro_group` ou `room_type`, volta `400`.
- **`GET|POST /generate_charts`**: gera os onze gráficos e devolve cada um em base64. A primeira chamada demora uns 8 segundos; as próximas saem do cache em memória e voltam na hora. Use `?refresh=1` para forçar o redesenho — necessário depois de trocar o CSV.
- **`GET /health`**: `{"status": "ok", "listings": N}`. Confere só se o CSV carregou; não chega a tocar no modelo.

---

<h2 align="center">🧪 Testes 🧪</h2>

Os testes sobem a aplicação com o CSV e o modelo de verdade, então cobrem também
a integração entre os módulos:

```bash
pip install -r requirements-dev.txt
pytest
```

---

<h2 align="center">🔍 Importações e Pacotes Utilizados 🔍</h2>

Aqui estão as principais bibliotecas utilizadas no projeto:

- **Pandas**: Manipulação e análise de dados.
- **NumPy**: Operações numéricas eficientes.
- **Matplotlib e Seaborn**: Visualização de dados.
- **Scikit-learn**: Pré-processamento, modelagem e avaliação do modelo.
- **Flask**: Criação da API para servir o modelo preditivo.

---

<h2 align="center">🚀 Como Funciona a Previsão? 🚀</h2>

O modelo utiliza um pipeline que inclui:
1. **Pré-processamento**:
   - Tratamento de valores ausentes com `SimpleImputer`.
   - Codificação de variáveis categóricas com `OneHotEncoder`.
   - Padronização de variáveis numéricas com `StandardScaler`.
2. **Modelo**:
   - Um `RandomForestRegressor` é usado para prever os preços com base nas características fornecidas.
3. **Avaliação**:
   - O desempenho do modelo é avaliado com RMSE (Root Mean Squared Error), MAE (Mean Absolute Error) e R², impressos no terminal ao final do treinamento.

---
