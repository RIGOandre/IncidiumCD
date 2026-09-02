import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "app"))

import app as flask_app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    flask_app.app.config.update(TESTING=True)
    return flask_app.app.test_client()


@pytest.fixture(scope="session")
def anuncio(client):
    """Um registro real vindo da busca, usado como entrada da previsao."""
    resultados = client.get("/search?q=skylit").get_json()
    assert resultados, "a busca precisa devolver ao menos um anuncio"
    return resultados[0]
