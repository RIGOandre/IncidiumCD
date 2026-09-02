"""API Flask do Indicium Price Predictor.

Rotas:
    GET  /                 tela de busca
    GET  /graph            pagina com os graficos da EDA
    GET  /search?q=        busca anuncios pelo nome
    POST /predict          preve o preco de um anuncio
    GET|POST /generate_charts   devolve os graficos em base64
    GET  /health           checagem rapida de que dados e modelo subiram
"""

import logging
import os

from flask import Flask, jsonify, render_template, request

import charts
from config import SEARCH_LIMIT
from dataset import load_dataset, search_listings, top_prices
from model import load_model, predict_price

logging.basicConfig(
    level=os.getenv("INCIDIUM_LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

_data = None
_model = None


def get_data():
    """CSV carregado uma unica vez por processo."""
    global _data
    if _data is None:
        _data = load_dataset()
    return _data


def get_model():
    """Pipeline treinado carregado uma unica vez por processo."""
    global _model
    if _model is None:
        _model = load_model()
    return _model


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/graph")
def graph():
    return render_template("graph.html", charts=charts.TITLES)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    return jsonify(search_listings(get_data(), query, SEARCH_LIMIT))


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Corpo da requisicao precisa ser JSON."}), 400

    try:
        preco = predict_price(get_model(), payload)
    except ValueError as erro:
        return jsonify({"error": str(erro)}), 400
    except Exception:
        logger.exception("Falha ao prever o preco")
        return jsonify({"error": "Nao foi possivel calcular a previsao."}), 500

    return jsonify({"prediction": f"${preco:,.2f}", "value": round(preco, 2)})


@app.route("/generate_charts", methods=["GET", "POST"])
def generate_charts():
    # ?refresh=1 forca o redesenho, util depois de trocar o CSV.
    refresh = request.args.get("refresh") in {"1", "true", "yes"}
    try:
        return jsonify(charts.generate_all(get_data(), refresh=refresh))
    except Exception:
        logger.exception("Falha ao gerar os graficos")
        return jsonify({"error": "Nao foi possivel gerar os graficos."}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "listings": len(get_data())})


def main():
    # Carrega tudo antes de abrir a porta: erro de caminho aparece agora,
    # e nao no meio da primeira requisicao.
    dados = get_data()
    get_model()

    logger.info("Dez anuncios mais caros:\n%s", top_prices(dados).to_string(index=False))

    app.run(
        host=os.getenv("INCIDIUM_HOST", "127.0.0.1"),
        port=int(os.getenv("INCIDIUM_PORT", "5000")),
        debug=os.getenv("INCIDIUM_DEBUG", "1") == "1",
    )


if __name__ == "__main__":
    main()
