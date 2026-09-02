"""Geracao dos graficos da analise exploratoria.

Cada funcao devolve um PNG em base64, pronto para virar src de <img>.
O conjunto completo fica em cache: sao onze figuras sobre ~49 mil linhas e
antes elas eram redesenhadas a cada visita da pagina /graph.
"""

import base64
import io
import logging
import re
import threading
from contextlib import contextmanager

import matplotlib

matplotlib.use("Agg")  # backend sem interface grafica, obrigatorio no servidor

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from config import EDA_NUMERIC_FEATURES, EXPENSIVE_LISTING_THRESHOLD

logger = logging.getLogger(__name__)

# Palavras muito comuns que poluem o ranking de anuncios caros.
STOPWORDS = {"by", "br", "the", "of"}

_cache = {}
_lock = threading.Lock()


@contextmanager
def _figure(figsize):
    """Cria a figura e garante o fechamento mesmo se o desenho falhar."""
    fig = plt.figure(figsize=figsize)
    try:
        yield fig
    finally:
        plt.close(fig)


def _to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def price_distribution(data):
    """Distribuicao de precos."""
    with _figure((12, 6)) as fig:
        sns.histplot(data["price"], bins=50, kde=True, color="black")
        plt.xlabel("Preco")
        plt.ylabel("Frequencia")
        return _to_base64(fig)


def avg_price_by_neighborhood(data):
    """Preco medio por bairro (um rotulo a cada dois, para caber no eixo)."""
    medias = data.groupby("bairro")["price"].mean().sort_values(ascending=False)
    bairros = medias.index[::2]
    valores = medias.values[::2]

    with _figure((25, 12)) as fig:
        sns.barplot(x=bairros, y=valores, hue=bairros, palette="viridis", width=0.5, legend=False)
        plt.xticks(rotation=90)
        plt.xlabel("Bairro", fontsize=24)
        plt.ylabel("Preco Medio", fontsize=24)
        plt.tick_params(axis="both", labelsize=18, pad=20)
        plt.tight_layout()
        plt.margins(x=0.01)
        plt.subplots_adjust(bottom=0.4)
        return _to_base64(fig)


def correlation_matrix(data):
    """Correlacao entre as variaveis numericas."""
    matriz = data[EDA_NUMERIC_FEATURES].corr()

    with _figure((10, 10)) as fig:
        sns.heatmap(matriz, annot=True, cmap="coolwarm", fmt=".2f")
        plt.subplots_adjust(bottom=0.4, left=0.3)
        return _to_base64(fig)


def room_type_vs_price(data):
    """Preco por tipo de quarto."""
    with _figure((10, 6)) as fig:
        sns.boxplot(data=data, x="room_type", y="price", hue="room_type", palette="Set2", legend=False)
        plt.xlabel("Tipo de Quarto")
        plt.ylabel("Preco")
        return _to_base64(fig)


def min_nights_vs_price(data):
    """Minimo de noites x preco, colorido pela disponibilidade."""
    with _figure((10, 6)) as fig:
        sns.scatterplot(data=data, x="minimo_noites", y="price", hue="disponibilidade_365", palette="viridis")
        plt.xlabel("Minimo de Noites")
        plt.ylabel("Preco")
        return _to_base64(fig)


def price_boxplot(data):
    """Boxplot dos precos, para enxergar os outliers."""
    with _figure((10, 6)) as fig:
        sns.boxplot(x=data["price"], color="orange")
        plt.xlabel("Preco")
        return _to_base64(fig)


def reviews_per_month(data):
    """Distribuicao de reviews por mes."""
    with _figure((14, 6)) as fig:
        sns.histplot(data["reviews_por_mes"].dropna(), bins=60, kde=True, color="green")
        plt.xlabel("Reviews por Mes")
        plt.ylabel("Frequencia")
        return _to_base64(fig)


def top_hosts(data):
    """Dez anfitrioes com mais anuncios."""
    ranking = data["host_name"].value_counts().head(10)

    with _figure((12, 8)) as fig:
        sns.barplot(x=ranking.index, y=ranking.values, hue=ranking.index, palette="Blues_d", legend=False)
        plt.xlabel("Host Name")
        plt.ylabel("Numero de Listagens")
        plt.xticks(rotation=45)
        return _to_base64(fig)


def rentability_index(data):
    """Indice de rentabilidade por bairro: preco medio sobre disponibilidade."""
    resumo = (
        data.groupby("bairro")
        .agg({"price": "mean", "disponibilidade_365": "mean"})
        .reset_index()
    )
    # Bairro com disponibilidade media zero geraria divisao por zero.
    resumo["rentability_index"] = (resumo["price"] / resumo["disponibilidade_365"]) * 100
    resumo = resumo.replace([np.inf, -np.inf], np.nan).dropna(subset=["rentability_index"])
    resumo = resumo.sort_values(by="rentability_index", ascending=False)

    bairros = resumo["bairro"][::2]
    valores = resumo["rentability_index"][::2]

    with _figure((30, 16)) as fig:
        sns.barplot(x=bairros, y=valores, hue=bairros, palette="Greens_d", width=0.5, legend=False)
        plt.xticks(rotation=90, fontsize=18)
        plt.tick_params(axis="x", pad=20)
        plt.xlabel("Bairro", fontsize=26)
        plt.ylabel("Indice de Rentabilidade", fontsize=30)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.3)
        return _to_base64(fig)


def word_price_relationship(data):
    """Palavras mais repetidas nos titulos dos anuncios caros."""
    caros = data[data["price"] > EXPENSIVE_LISTING_THRESHOLD]

    def palavras(titulo):
        titulo = str(titulo).lower()
        titulo = re.sub(r"[^a-z\s]", "", titulo)  # fora numeros e pontuacao
        return titulo.split()

    contagem = caros["nome"].apply(palavras).explode().value_counts()
    contagem = contagem[~contagem.index.isin(STOPWORDS)].head(10)

    with _figure((10, 6)) as fig:
        sns.barplot(x=contagem.values, y=contagem.index, hue=contagem.index, palette="Blues_d", legend=False)
        plt.xlabel("Frequencia", fontsize=16)
        plt.ylabel("Palavras", fontsize=16)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.tight_layout()
        return _to_base64(fig)


def investment_opportunities(data):
    """Rentabilidade x demanda por bairro, com o tamanho do ponto no volume."""
    resumo = (
        data.groupby("bairro")
        .agg({"price": "mean", "reviews_por_mes": "mean", "host_name": "count"})
        .reset_index()
    )
    resumo["rentability"] = resumo["price"] / resumo["reviews_por_mes"]
    resumo = resumo.replace([np.inf, -np.inf], np.nan).dropna()

    with _figure((12, 8)) as fig:
        sns.scatterplot(
            data=resumo,
            x="rentability",
            y="reviews_por_mes",
            size="host_name",
            sizes=(50, 500),
            hue="host_name",
            palette="viridis",
            alpha=0.7,
        )
        plt.xlabel("Rentabilidade (Preco Medio / Reviews por Mes)", fontsize=16)
        plt.ylabel("Demanda (Reviews por Mes)", fontsize=16)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.legend(title="Numero de Listagens", fontsize=12)
        plt.tight_layout()
        return _to_base64(fig)


# Ordem de exibicao e titulo de cada grafico em graph.html.
CHARTS = {
    "price_distribution": price_distribution,
    "avg_price_by_neighborhood": avg_price_by_neighborhood,
    "correlation_matrix": correlation_matrix,
    "room_type_vs_price": room_type_vs_price,
    "min_nights_vs_price": min_nights_vs_price,
    "price_boxplot": price_boxplot,
    "reviews_per_month": reviews_per_month,
    "top_hosts": top_hosts,
    "rentability_index": rentability_index,
    "word_price_relationship": word_price_relationship,
    "investment_opportunities": investment_opportunities,
}

TITLES = {
    "price_distribution": "Distribuição de Preços",
    "avg_price_by_neighborhood": "Preço Médio por Bairro",
    "correlation_matrix": "Matriz de Correlação",
    "room_type_vs_price": "Relação entre Tipo de Quarto e Preço",
    "min_nights_vs_price": "Relação entre Mínimo de Noites, Disponibilidade e Preço",
    "price_boxplot": "Boxplot dos Preços (Outliers)",
    "reviews_per_month": "Distribuição de Reviews por Mês",
    "top_hosts": "Top 10 Hosts com Mais Listagens",
    "rentability_index": "Rentabilidade",
    "word_price_relationship": "Palavras Mais Frequentes em Anúncios Caros (> $5000)",
    "investment_opportunities": "Melhores Lugares para Investir",
}


def generate_all(data, refresh=False):
    """Gera (ou reaproveita) todos os graficos em base64.

    O lock evita que duas requisicoes simultaneas desenhem no mesmo estado
    global do matplotlib.
    """
    with _lock:
        if _cache and not refresh:
            return dict(_cache)

        resultado = {}
        for nome, funcao in CHARTS.items():
            logger.info("Gerando grafico %s", nome)
            resultado[nome] = funcao(data)

        _cache.clear()
        _cache.update(resultado)
        return dict(resultado)
