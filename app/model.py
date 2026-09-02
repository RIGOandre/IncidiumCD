"""Carga do modelo treinado e preparo da entrada de previsao."""

import gzip
import logging
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    CATEGORICAL_FEATURES,
    MODEL_CANDIDATES,
    MODEL_FEATURES,
    MODEL_PATH,
    NUMERIC_FEATURES,
    REQUIRED_FEATURES,
)

logger = logging.getLogger(__name__)


def _resolve_model_path():
    if MODEL_PATH:
        return Path(MODEL_PATH)

    for candidate in MODEL_CANDIDATES:
        if candidate.exists():
            return candidate

    procurados = ", ".join(str(path) for path in MODEL_CANDIDATES)
    raise FileNotFoundError(
        f"Modelo nao encontrado (procurado em: {procurados}). "
        "Rode notebooks/treinamento_modelo.py para gerar o arquivo."
    )


def load_model():
    """Carrega o pipeline treinado, aceitando .pkl.gz ou .pkl."""
    path = _resolve_model_path()
    opener = gzip.open if path.suffix == ".gz" else open

    with opener(path, "rb") as handle:
        model = pickle.load(handle)

    logger.info("Modelo carregado de %s", path)
    return model


def build_features(payload):
    """Monta o DataFrame de uma linha esperado pelo pipeline.

    A tela envia o registro inteiro do anuncio. Aqui ficam so as colunas do
    treino, os numeros voltam a ser numeros e o que faltar entra como NaN,
    para o SimpleImputer completar. Antes, um payload sem alguma coluna
    derrubava a rota com "columns are missing".
    """
    if not isinstance(payload, dict):
        raise ValueError("Envie um objeto JSON com os dados do anuncio.")

    ausentes = [
        feature
        for feature in REQUIRED_FEATURES
        if payload.get(feature) is None or payload.get(feature) == ""
    ]
    if ausentes:
        raise ValueError(
            "Faltam colunas obrigatorias no anuncio: " + ", ".join(ausentes) + "."
        )

    frame = pd.DataFrame([{feature: payload.get(feature) for feature in MODEL_FEATURES}])

    for column in NUMERIC_FEATURES:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    for column in CATEGORICAL_FEATURES:
        coluna = frame[column].astype(object)
        frame[column] = coluna.where(coluna.notna(), np.nan)

    return frame


def predict_price(model, payload):
    """Devolve o preco previsto para um anuncio."""
    prediction = model.predict(build_features(payload))
    return float(prediction[0])
