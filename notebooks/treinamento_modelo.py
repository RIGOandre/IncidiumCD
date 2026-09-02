"""Treinamento do modelo de precificacao.

Rode de qualquer diretorio:

    python notebooks/treinamento_modelo.py

O pipeline treinado e salvo compactado em model.pkl.gz, na raiz do projeto,
que e o arquivo que a API carrega.
"""

import gzip
import pickle
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# - `pandas`: manipulacao e leitura dos dados.
# - `train_test_split`: divide os dados em treino e teste.
# - `RandomForestRegressor`: modelo de regressao baseado em arvores de decisao.
# - `root_mean_squared_error` e companhia: metricas de avaliacao.
# - `OneHotEncoder` e `StandardScaler`: pre-processamento de variaveis
#   categoricas e numericas.
# - `ColumnTransformer` e `Pipeline`: pipelines modulares de pre-processamento
#   e modelagem.
# - `SimpleImputer`: tratamento de valores ausentes.
# - `gzip` + `pickle`: gravam o modelo treinado (compactado, o model.pkl.gz
#   fica com uns 54 MB - o numero muda conforme o dataset e a floresta,
#   entao confira de novo antes de citar um valor aqui).

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "teste_indicium_precificacao.csv"
MODEL_PATH = PROJECT_ROOT / "model.pkl.gz"

# Caminhos derivados da posicao deste arquivo: antes havia um caminho absoluto
# da maquina do autor, que quebrava em qualquer outro computador.

NUMERIC_FEATURES = [
    "latitude",
    "longitude",
    "minimo_noites",
    "numero_de_reviews",
    "reviews_por_mes",
    "calculado_host_listings_count",
    "disponibilidade_365",
]
CATEGORICAL_FEATURES = ["bairro_group", "bairro", "room_type"]

# Colunas descartadas: identificadores e textos livres nao ajudam a prever o
# preco (`price` e o alvo).
DROP_COLUMNS = ["price", "id", "host_id", "host_name", "nome", "ultima_review"]

RANDOM_STATE = 42
TEST_SIZE = 0.2


def build_pipeline():
    """Pre-processamento + Random Forest em um unico objeto."""
    # Numericas: NaN pela media e padronizacao.
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler()),
        ]
    )

    # Categoricas: NaN pela moda e One-Hot Encoding.
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # O ColumnTransformer aplica cada transformacao nas colunas certas.
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    # Juntar pre-processamento e modelo garante que treino e inferencia
    # apliquem exatamente as mesmas transformacoes.
    # n_jobs=-1 usa todos os nucleos: o treino cai de minutos para segundos
    # em maquinas com varios processadores.
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)),
        ]
    )


def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV nao encontrado: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print(f"{len(df)} anuncios carregados de {CSV_PATH.name}")

    X = df.drop(columns=DROP_COLUMNS)
    y = df["price"]

    # 80% treino / 20% teste, com semente fixa para o resultado ser reproduzivel.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    model = build_pipeline()
    print("Treinando...")
    model.fit(X_train, y_train)

    # O RMSE penaliza erros grandes; o MAE mostra o erro tipico em dolares e
    # o R2 indica quanto da variacao do preco o modelo consegue explicar.
    y_pred = model.predict(X_test)
    print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.2f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"R2:   {r2_score(y_test, y_pred):.4f}")

    with gzip.open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Modelo salvo em {MODEL_PATH}")


if __name__ == "__main__":
    main()
