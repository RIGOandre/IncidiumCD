"""Caminhos e parametros centrais do projeto.

Tudo e resolvido a partir da localizacao deste arquivo, entao a aplicacao
roda de qualquer diretorio (antes so funcionava com o cwd dentro de app/).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
CSV_PATH = Path(os.getenv("INCIDIUM_CSV", DATA_DIR / "teste_indicium_precificacao.csv"))

# O modelo versionado no repositorio esta compactado; o .pkl cru e aceito
# como alternativa para quem acabou de rodar o treinamento.
MODEL_CANDIDATES = (
    PROJECT_ROOT / "model.pkl.gz",
    PROJECT_ROOT / "model.pkl",
)
MODEL_PATH = os.getenv("INCIDIUM_MODEL")

# Colunas usadas no treino (notebooks/treinamento_modelo.py).
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
MODEL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# Sem estas colunas a previsao nao significa nada: o imputer preencheria o resto
# e o modelo devolveria a media do treino com cara de resposta. A tela sempre
# manda o registro inteiro vindo da busca, entao exigir as quatro nao atrapalha
# o uso normal - so barra payload aleatorio.
REQUIRED_FEATURES = ["latitude", "longitude", "bairro_group", "room_type"]

# Colunas numericas usadas apenas na analise exploratoria.
EDA_NUMERIC_FEATURES = [
    "latitude",
    "longitude",
    "price",
    "minimo_noites",
    "numero_de_reviews",
    "reviews_por_mes",
    "calculado_host_listings_count",
    "disponibilidade_365",
]

# Limite de resultados devolvidos pela busca.
SEARCH_LIMIT = int(os.getenv("INCIDIUM_SEARCH_LIMIT", "15"))

# Preco a partir do qual um anuncio e considerado caro na analise de palavras.
EXPENSIVE_LISTING_THRESHOLD = 5000
