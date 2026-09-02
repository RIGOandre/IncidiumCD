"""Carga e preparo do CSV de anuncios."""

import logging

import pandas as pd

from config import CSV_PATH, NUMERIC_FEATURES

logger = logging.getLogger(__name__)

# Coluna auxiliar minuscula: a busca usa ela, a exibicao continua usando 'nome'
# com a grafia original.
SEARCH_COLUMN = "nome_busca"


def load_dataset(csv_path=CSV_PATH):
    """Le o CSV e devolve o DataFrame pronto para busca e graficos."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV nao encontrado: {csv_path}. "
            "Confira a pasta data/ ou aponte INCIDIUM_CSV para outro arquivo."
        )

    data = pd.read_csv(csv_path)
    data["nome"] = data["nome"].fillna("")
    data[SEARCH_COLUMN] = data["nome"].str.lower()

    # Garante tipo numerico mesmo com celulas vazias no CSV.
    for column in NUMERIC_FEATURES:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    logger.info("Dados carregados: %d anuncios de %s", len(data), csv_path)
    return data


def search_listings(data, query, limit):
    """Busca anuncios por trecho do nome.

    O termo entra como texto literal (regex=False): sem isso qualquer '(' ou
    '*' digitado pelo usuario quebrava a rota com erro de expressao regular.
    """
    query = (query or "").strip().lower()
    if not query:
        return []

    matches = data[data[SEARCH_COLUMN].str.contains(query, regex=False, na=False)]
    matches = matches.head(limit).drop(columns=[SEARCH_COLUMN])

    # NaN nao existe em JSON; vira null.
    return matches.astype(object).where(pd.notna(matches), None).to_dict(orient="records")


def top_prices(data, n=10):
    """Anuncios mais caros - usado no log de inicializacao."""
    return data.nlargest(n, "price")[["host_name", "price", "bairro"]]
