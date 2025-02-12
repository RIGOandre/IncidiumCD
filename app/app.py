import re
from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import threading
import tkinter as tk
from matplotlib.ticker import MaxNLocator

app = Flask(__name__)

def tkinter_thread():
    root = tk.Tk()
    root.mainloop()

# Carregar o modelo treinado
with open('../model.pkl', 'rb') as f:
    model = pickle.load(f)

# Definir o caminho relativo para o CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'teste_indicium_precificacao.csv')
print(f"Caminho do CSV: {CSV_PATH}")

# Verificar se o arquivo existe
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Arquivo CSV não encontrado: {CSV_PATH}")

# Carregar o CSV
try:
    data = pd.read_csv(CSV_PATH)
except Exception as e:
    raise RuntimeError(f"Erro ao carregar o CSV: {e}")

# Tratar valores nulos na coluna 'nome'
data['nome'] = data['nome'].fillna('').str.lower()
data = data.set_index('nome', drop=False)
print("Dados carregados com sucesso:")
print(data.head())

# Função para salvar gráficos como Base64
def save_plot_as_base64():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

# Distribuição de Preços
def generate_price_distribution():
    plt.figure(figsize=(12, 6))
    sns.histplot(data['price'], bins=50, kde=True, color='black')
    # plt.title('Distribuição dos Preços')
    plt.xlabel('Preço')
    plt.ylabel('Frequência')
    return save_plot_as_base64()

# Preço Médio por Bairro
def generate_avg_price_by_neighborhood():
    avg_price_by_neighborhood = data.groupby('bairro')['price'].mean().sort_values(ascending=False)
    
    # Filtrar rótulos (opcional)
    indices_filtrados = avg_price_by_neighborhood.index[::2]  # Exibe a cada 2 bairros
    valores_filtrados = avg_price_by_neighborhood.values[::2]
    
    plt.figure(figsize=(25, 12))  
    sns.barplot(x=indices_filtrados, y=valores_filtrados, palette='viridis', width=0.5)
    
    plt.xticks(rotation=90)
    # plt.title('Preço Médio por Bairro', fontsize=34)
    plt.xlabel('Bairro', fontsize=24)
    plt.ylabel('Preço Médio', fontsize=24)
    
    # Ajustar o tamanho da fonte e o espaçamento
    plt.tick_params(axis='both', labelsize=18, pad=20) 
    plt.tight_layout()
    plt.margins(x=0.01)
    plt.subplots_adjust(bottom=0.4)  
    
    return save_plot_as_base64()

# Matriz de Correlação

def generate_correlation_matrix():
    numeric_features = ['latitude', 'longitude', 'price', 'minimo_noites', 'numero_de_reviews',
                        'reviews_por_mes', 'calculado_host_listings_count', 'disponibilidade_365']
    correlation_matrix = data[numeric_features].corr()
    plt.figure(figsize=(10, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    # plt.title('Matriz de Correlação entre Variáveis Numéricas')
    plt.subplots_adjust(bottom=0.4,left=0.3)
    return save_plot_as_base64()

# Relação entre Tipo de Quarto e Preço

def generate_room_type_vs_price():
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x='room_type', y='price', palette='Set2')
    # plt.title('Relação entre Tipo de Quarto e Preço')
    plt.xlabel('Tipo de Quarto')
    plt.ylabel('Preço')
    return save_plot_as_base64()

# Relação entre Mínimo de Noites, Disponibilidade e Preço

def generate_min_nights_vs_price():
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='minimo_noites', y='price', hue='disponibilidade_365', palette='viridis')
    # plt.title('Relação entre Mínimo de Noites, Disponibilidade e Preço')
    plt.xlabel('Mínimo de Noites')
    plt.ylabel('Preço')
    return save_plot_as_base64()

# Boxplot dos Preços (Outliers)

def generate_price_boxplot():
    plt.figure(figsize=(10, 6))
    sns.boxplot(data['price'], color='orange')
    # plt.title('Boxplot dos Preços')
    plt.xlabel('Preço')
    return save_plot_as_base64()

# Distribuição de Reviews por Mês
def generate_reviews_per_month():
    plt.figure(figsize=(14, 6))
    sns.histplot(data['reviews_por_mes'], bins=60, kde=True, color='green')
    # plt.title('Distribuição de Reviews por Mês')
    plt.xlabel('Reviews por Mês')
    plt.ylabel('Frequência')
    return save_plot_as_base64()

# Top 10 Hosts com Mais Listagens
def generate_top_hosts():
    top_hosts = data['host_name'].value_counts().head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_hosts.index, y=top_hosts.values, palette='Blues_d')
    plt.xlabel('Host Name')
    plt.ylabel('Número de Listagens')
    plt.xticks(rotation=45)
    return save_plot_as_base64()

# Índice de Rentabilidade por Bairro
def generate_rentability_index():
    # Calcular o índice de rentabilidade: preço médio / disponibilidade média
    rentability_index = (
        data.groupby('bairro')
        .agg({'price': 'mean', 'disponibilidade_365': 'mean'})
        .reset_index()
    )
    rentability_index['rentability_index'] = (rentability_index['price'] / rentability_index['disponibilidade_365']) * 100
    rentability_index = rentability_index.sort_values(by='rentability_index', ascending=False)
    indices_filtrados = rentability_index['bairro'][::2]  #  cada 2 bairros
    valores_filtrados = rentability_index['rentability_index'][::2]

    # Plotar o gráfico
    plt.figure(figsize=(30, 16))  
    sns.barplot(x=indices_filtrados, y=valores_filtrados, palette='Greens_d', width=0.5)

    # Ajustar os rótulos do eixo x
    plt.xticks(rotation=90, fontsize=18)  
    plt.tick_params(axis='x', pad=20)  

    # Título e rótulos dos eixos
    # plt.title('Índice de Rentabilidade por Bairro', fontsize=34)
    plt.xlabel('Bairro', fontsize=26)
    plt.ylabel('Índice de Rentabilidade', fontsize=30)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)  

    return save_plot_as_base64()

def generate_word_price_relationship():
    # Filtrar anúncios caros (preço > 300)
    expensive_listings = data[data['price'] > 5000]
    
    # Processar os nomes dos anúncios para extrair palavras
    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)  
        words = text.split() 
        return words

    # Aplicar a função de pré-processamento aos nomes dos anúncios caros
    words = expensive_listings['nome'].apply(preprocess_text).explode()

    word_counts = words.value_counts()

    words_to_exclude = {"by", "br", "the", "of"}
    filtered_word_counts = word_counts[~word_counts.index.isin(words_to_exclude)]

    filtered_word_counts = filtered_word_counts.head(10)

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x=filtered_word_counts.values, y=filtered_word_counts.index, palette='Blues_d')
    # plt.title('Palavras Mais Frequentes em Anúncios Caros', fontsize=20)
    plt.xlabel('Frequência', fontsize=16)
    plt.ylabel('Palavras', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    # Salvar o gráfico como Base64
    return save_plot_as_base64()

# Rota para gerar gráficos
@app.route('/generate_charts', methods=['POST'])
def generate_charts():
    try:

        price_distribution = generate_price_distribution()
        avg_price_by_neighborhood = generate_avg_price_by_neighborhood()
        correlation_matrix = generate_correlation_matrix()
        room_type_vs_price = generate_room_type_vs_price()
        min_nights_vs_price = generate_min_nights_vs_price()
        price_boxplot = generate_price_boxplot()
        reviews_per_month = generate_reviews_per_month()
        top_hosts = generate_top_hosts()
        rentability_index = generate_rentability_index() 
        word_price_relationship = generate_word_price_relationship()

        # Retornar os dados como JSON
        response_data = {
            "price_distribution": price_distribution,
            "avg_price_by_neighborhood": avg_price_by_neighborhood,
            "correlation_matrix": correlation_matrix,
            "room_type_vs_price": room_type_vs_price,
            "min_nights_vs_price": min_nights_vs_price,
            "price_boxplot": price_boxplot,
            "reviews_per_month": reviews_per_month,
            "top_hosts": top_hosts,
            "rentability_index": rentability_index,
            "word_price_relationship": word_price_relationship
        }
        return jsonify(response_data)
    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")
        return jsonify({"error": str(e)}), 500

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para buscar hotéis
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    results = data[data.index.str.startswith(query)]
    results = results.to_dict(orient='records')
    return jsonify(results)

# Rota para prever o preço
@app.route('/predict', methods=['POST'])
def predict():
    data_json = request.json
    df = pd.DataFrame([data_json])
    prediction = model.predict(df)
    return jsonify({"prediction": f"${prediction[0]:.2f}"})

# Rota para a página de gráficos
@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True)