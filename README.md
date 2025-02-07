<h1 align="center">🏠 Indicium Price Predictor 🏠</h1>

<p align="center">
  <strong>Um modelo preditivo para prever preços de aluguéis temporários em Nova York! 🌆</strong>
</p>

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
- **Entrega Final**: Organizar o projeto em um repositório público com documentação clara e instruções de instalação.

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

Para executar este projeto, você precisará dos seguintes pacotes e suas versões:

```plaintext
Python == 3.13
pandas == 2.0.3
numpy == 1.24.3
scikit-learn == 1.6.1
matplotlib == 3.7.2
seaborn == 0.12.2
flask == 2.3.2
```

Você pode instalar todas as dependências usando o arquivo `requirements.txt` fornecido no repositório.

---

<h2 align="center">📚 Passo a Passo para Instalação 📚</h2>

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/indicium-price-predictor.git
   cd indicium-price-predictor
   ```

2. **Crie um Ambiente Virtual (Opcional, mas Recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Treine o Modelo**:
   - Execute o notebook `notebooks/model_training.ipynb` para treinar e salvar o modelo (`model.pkl`).

5. **Execute a API Flask**:
   - Inicie a API Flask com o seguinte comando:
     ```bash
     python app/app.py
     ```
   - Acesse a interface no navegador em `http://127.0.0.1:5000/`.

6. **Teste o Modelo**:
   - Insira os dados do apartamento na interface HTML e veja a previsão de preço.

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

<p align="center">
  🌟 <strong>Desenvolvido para simplificar a precificação de aluguéis temporários e fornecer insights valiosos para o negócio!</strong> 🌟
</p>
