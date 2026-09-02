"""Testes das rotas HTTP.

Rodam sobre o CSV e o modelo de verdade do repositorio, entao cobrem tambem a
integracao entre dataset, model e as rotas.
"""

import config


def test_home_responde(client):
    assert client.get("/").status_code == 200


def test_graph_responde(client):
    assert client.get("/graph").status_code == 200


def test_health_informa_quantidade(client):
    corpo = client.get("/health").get_json()

    assert corpo["status"] == "ok"
    assert corpo["listings"] > 0


def test_busca_encontra_anuncios(client):
    resultados = client.get("/search?q=skylit").get_json()

    assert resultados
    assert all("nome" in item for item in resultados)


def test_busca_respeita_o_limite(client):
    resultados = client.get("/search?q=a").get_json()

    assert len(resultados) <= config.SEARCH_LIMIT


def test_busca_nao_devolve_a_coluna_auxiliar(client):
    # nome_busca existe so para a comparacao em minusculas.
    resultados = client.get("/search?q=loft").get_json()

    assert all("nome_busca" not in item for item in resultados)


def test_busca_vazia_devolve_lista_vazia(client):
    assert client.get("/search?q=").get_json() == []
    assert client.get("/search?q=%20%20").get_json() == []


def test_busca_aceita_caractere_de_regex(client):
    # Um parenteses no termo quebrava a rota com erro de expressao regular.
    resposta = client.get("/search?q=a(b")

    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_previsao_de_um_anuncio_real(client, anuncio):
    corpo = client.post("/predict", json=anuncio).get_json()

    assert corpo["value"] > 0
    assert corpo["prediction"].startswith("$")


def test_previsao_recusa_corpo_que_nao_e_json(client):
    resposta = client.post("/predict", data="isto nao e json",
                           content_type="text/plain")

    assert resposta.status_code == 400


def test_previsao_recusa_anuncio_sem_as_colunas_obrigatorias(client):
    # Sem estas colunas o imputer preencheria tudo e o modelo devolveria a media
    # do treino como se fosse uma previsao daquele anuncio.
    resposta = client.post("/predict", json={"lixo": 1})

    assert resposta.status_code == 400
    assert "obrigatorias" in resposta.get_json()["error"]


def test_previsao_recusa_anuncio_com_coluna_obrigatoria_vazia(client, anuncio):
    incompleto = dict(anuncio)
    incompleto["room_type"] = None

    resposta = client.post("/predict", json=incompleto)

    assert resposta.status_code == 400
    assert "room_type" in resposta.get_json()["error"]
