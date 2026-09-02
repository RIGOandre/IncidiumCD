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
   - O desempenho do modelo é avaliado usando RMSE (Root Mean Squared Error).

---
