"""Testes dos modulos de dados e de modelo, sem passar pelas rotas."""

import math

import pandas as pd
import pytest

import config
import dataset
import model


def test_dataset_carrega_e_cria_a_coluna_de_busca(client):
    # A fixture client ja subiu a aplicacao, entao os dados estao em memoria.
    import app as flask_app

    dados = flask_app.get_data()

    assert len(dados) > 0
    assert dataset.SEARCH_COLUMN in dados.columns
    assert dados["nome"].isna().sum() == 0


def test_busca_ignora_maiusculas():
    dados = pd.DataFrame(
        {
            "nome": ["Loft Aconchegante", "Casa na Praia"],
            "price": [100, 200],
            "host_name": ["Ana", "Bruno"],
            "bairro": ["Centro", "Litoral"],
        }
    )
    dados[dataset.SEARCH_COLUMN] = dados["nome"].str.lower()

    achados = dataset.search_listings(dados, "LOFT", limit=10)

    assert len(achados) == 1
    assert achados[0]["nome"] == "Loft Aconchegante"


def test_busca_troca_nan_por_none():
    # NaN nao existe em JSON: precisa sair como null.
    dados = pd.DataFrame({"nome": ["Studio"], "reviews_por_mes": [float("nan")]})
    dados[dataset.SEARCH_COLUMN] = dados["nome"].str.lower()

    achados = dataset.search_listings(dados, "studio", limit=10)

    assert achados[0]["reviews_por_mes"] is None


def test_build_features_devolve_uma_linha_com_as_colunas_do_treino():
    payload = {feature: 1 for feature in config.MODEL_FEATURES}
    payload["bairro_group"] = "Manhattan"
    payload["bairro"] = "Harlem"
    payload["room_type"] = "Private room"

    frame = model.build_features(payload)

    assert len(frame) == 1
    assert list(frame.columns) == config.MODEL_FEATURES


def test_build_features_descarta_colunas_extras():
    payload = {feature: 1 for feature in config.MODEL_FEATURES}
    payload.update(bairro_group="Brooklyn", bairro="Bushwick",
                   room_type="Entire home/apt", id=999, host_name="Ana")

    frame = model.build_features(payload)

    assert "id" not in frame.columns
    assert "host_name" not in frame.columns


def test_build_features_converte_texto_numerico():
    payload = {feature: "1" for feature in config.MODEL_FEATURES}
    payload.update(bairro_group="Queens", bairro="Astoria", room_type="Private room")

    frame = model.build_features(payload)

    # "1" vira int e "1.5" vira float: o que importa e nao continuar texto.
    assert frame["latitude"].dtype.kind in "if"


def test_build_features_transforma_numero_invalido_em_nan():
    payload = {feature: 1 for feature in config.MODEL_FEATURES}
    payload.update(bairro_group="Bronx", bairro="Fordham",
                   room_type="Shared room", minimo_noites="nao e numero")

    frame = model.build_features(payload)

    assert math.isnan(frame["minimo_noites"].iloc[0])


def test_build_features_exige_as_colunas_obrigatorias():
    with pytest.raises(ValueError) as erro:
        model.build_features({"lixo": 1})

    for feature in config.REQUIRED_FEATURES:
        assert feature in str(erro.value)


def test_build_features_recusa_o_que_nao_e_dicionario():
    with pytest.raises(ValueError):
        model.build_features([1, 2, 3])
