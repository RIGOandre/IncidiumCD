import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

df = pd.read_csv(r'C:\Users\manoa\Documents\GitHub\IncidiumCD\data\teste_indicium_precificacao.csv')

def generate_price_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=50, kde=True, color='black')
    plt.title('Distribuição dos Preços')
    plt.xlabel('Preço')
    plt.ylabel('Frequência')
    
    # Salvar o gráfico em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

def generate_avg_price_by_neighborhood():
    avg_price_by_neighborhood = df.groupby('bairro')['price'].mean().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=avg_price_by_neighborhood.index, y=avg_price_by_neighborhood.values, palette='viridis')
    plt.xticks(rotation=90)
    plt.title('Preço Médio por Bairro')
    plt.xlabel('Bairro')
    plt.ylabel('Preço Médio')
    
    # Salvar o gráfico em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

def generate_correlation_matrix():
    numeric_features = ['latitude', 'longitude', 'price', 'minimo_noites', 'numero_de_reviews', 
                        'reviews_por_mes', 'calculado_host_listings_count', 'disponibilidade_365']
    correlation_matrix = df[numeric_features].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de Correlação entre Variáveis Numéricas')
    
    # Salvar o gráfico em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

# informações base dataset (n esc)
print("Informações básicas do dataset:")
print(df.info())
print("\nEstatísticas descritivas:")
print(df.describe())

# valores ausentes
print("\nValores ausentes por coluna:")
print(df.isnull().sum())

# distribuição de preços
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=50, kde=True, color='black')
plt.title('Distribuição dos Preços')
plt.xlabel('Preço')
plt.ylabel('Frequência')
plt.show()

# preço médio por bairro/bairro_group
avg_price_by_neighborhood = df.groupby('bairro')['price'].mean().sort_values(ascending=False)
avg_price_by_bairro_group = df.groupby('bairro_group')['price'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=avg_price_by_neighborhood.index, y=avg_price_by_neighborhood.values, palette='viridis')
plt.xticks(rotation=90)
plt.title('Preço Médio por Bairro')
plt.xlabel('Bairro')
plt.ylabel('Preço Médio')
plt.show()

plt.figure(figsize=(8, 6))
sns.barplot(x=avg_price_by_bairro_group.index, y=avg_price_by_bairro_group.values, palette='coolwarm')
plt.title('Preço Médio por Bairro Group')
plt.xlabel('Bairro Group')
plt.ylabel('Preço Médio')
plt.show()

# tipo de quarto e preço
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='room_type', y='price', palette='Set2')
plt.title('Relação entre Tipo de Quarto e Preço')
plt.xlabel('Tipo de Quarto')
plt.ylabel('Preço')
plt.show()

# correlação entre vn
numeric_features = ['latitude', 'longitude', 'price', 'minimo_noites', 'numero_de_reviews', 
                    'reviews_por_mes', 'calculado_host_listings_count', 'disponibilidade_365']

correlation_matrix = df[numeric_features].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matriz de Correlação entre Variáveis Numéricas')
plt.show()

# mínimo de noites e disponibilidade no preço
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='minimo_noites', y='price', hue='disponibilidade_365', palette='viridis')
plt.title('Relação entre Mínimo de Noites, Disponibilidade e Preço')
plt.xlabel('Mínimo de Noites')
plt.ylabel('Preço')
plt.show()

# outliers no preço
plt.figure(figsize=(10, 6))
sns.boxplot(df['price'], color='orange')
plt.title('Boxplot dos Preços')
plt.xlabel('Preço')
plt.show()

# distribuição de reviews por mês
plt.figure(figsize=(10, 6))
sns.histplot(df['reviews_por_mes'], bins=50, kde=True, color='green')
plt.title('Distribuição de Reviews por Mês')
plt.xlabel('Reviews por Mês')
plt.ylabel('Frequência')
plt.show()

# Top 10 com mais listagens
top_hosts = df['host_name'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_hosts.index, y=top_hosts.values, palette='Blues_d')
plt.title('Top 10 com Mais Listagens')
plt.xlabel('Host Name')
plt.ylabel('Número de Listagens')
plt.xticks(rotation=45)
plt.show()

#e2

# bairros com maior retorno financeiro
df['retorno_financeiro'] = df['price'] * df['disponibilidade_365']
m_i = df.groupby('bairro')['retorno_financeiro'].mean().sort_values(ascending=False)
print(m_i)

# min noites disp 365 + p
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='minimo_noites', y='price', hue='disponibilidade_365', palette='viridis')
plt.title('Relação entre Mínimo de Noites, Disponibilidade e Preço')
plt.show()

