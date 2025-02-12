import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pickle
import numpy as np  

# - `pandas`: Para manipulação e leitura dos dados.
# - `train_test_split`: Para dividir os dados em conjuntos de treino e teste.
# - `RandomForestRegressor`: Modelo de regressão baseado em árvores de decisão.
# - `mean_squared_error`: Métrica para avaliar o desempenho do modelo.
# - `OneHotEncoder` e `StandardScaler`: Pré-processamento de variáveis categóricas e numéricas.
# - `ColumnTransformer` e `Pipeline`: Para criar pipelines modulares de pré-processamento e modelagem.
# - `SimpleImputer`: Para lidar com valores ausentes.
# - `pickle`: Para salvar o modelo treinado.
# - `numpy`: Para operações matemáticas, como calcular a raiz quadrada do MSE.


df = pd.read_csv(r'C:\Users\manoa\Documents\GitHub\IncidiumCD\data\teste_indicium_precificacao.csv')



# Comentário:
# - Os dados são carregados de um arquivo CSV localizado no caminho especificado.
# - Este conjunto de dados contém informações sobre imóveis do Airbnb, incluindo características como localização, 
# tipo de quarto, disponibilidade e preço.

X = df.drop(columns=['price', 'id', 'host_id', 'host_name', 'nome', 'ultima_review'])
y = df['price']

# - `X`: Contém as variáveis independentes (características) usadas para prever o preço.
# - `y`: Contém a variável dependente (preço), que é o alvo da previsão.
# - Colunas como `id`, `host_id`, `host_name`, `nome` e `ultima_review` são descartadas porque 
# não contribuem diretamente para a previsão do preço.

numeric_features = ['latitude', 'longitude', 'minimo_noites', 'numero_de_reviews', 
                    'reviews_por_mes', 'calculado_host_listings_count', 'disponibilidade_365']
categorical_features = ['bairro_group', 'bairro', 'room_type']

# - `numeric_features`: Lista de variáveis numéricas que serão padronizadas.
# - `categorical_features`: Lista de variáveis categóricas que serão codificadas usando One-Hot Encoding.


numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  #  NaNs pela média
    ('scaler', StandardScaler())  # padronizar
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # substituir NaNs pela moda
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  #  one-Hot Encoding
])

# - Para variáveis numéricas, optamos por substituir valores ausentes pela média e padronizar os dados 
# para melhorar o desempenho do modelo.
# - Para variáveis categóricas, usamos a moda para substituir valores ausentes e aplicamos One-Hot 
# Encoding para transformar categorias em variáveis binárias.

# transformadores em um ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# - O `ColumnTransformer` combina os transformadores para variáveis numéricas e categóricas.
# - Ele aplica as transformações corretas às colunas correspondentes automaticamente.

# pipeline completo (pré-processamento + modelo)
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# - O pipeline combina o pré-processamento (`preprocessor`) e o modelo de regressão (`RandomForestRegressor`).
# - Isso garante que todas as transformações sejam aplicadas consistentemente durante o treinamento e a inferência.
# - O `RandomForestRegressor` foi escolhido por sua robustez e capacidade de lidar com dados heterogêneos.

# treino x teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# - Os dados são divididos em conjuntos de treino (80%) e teste (20%).
# - A divisão aleatória é controlada pelo `random_state` para garantir reprodutibilidade.


# treinar modelo
model.fit(X_train, y_train)
# - O modelo é treinado com os dados de treino.
# - O `fit` método é usado para ajustar os parâmetros do modelo para os dados de treino. 
# - O modelo agora está pronto para fazer previsões com os dados de teste.

# previsões no conjunto de teste
y_pred = model.predict(X_test)
# calcular RMSE manualmente
mse = mean_squared_error(y_test, y_pred) 
rmse = np.sqrt(mse)  
# exibir o RMSE
print(f'RMSE: {rmse}')

# - O RMSE (Root Mean Squared Error) é calculado para avaliar o desempenho do modelo.
# - O RMSE mede a diferença média entre os valores previstos e reais, penalizando erros maiores.

# salvar o modelo treinado em um arquivo .pkl
with open('../model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Modelo treinado e salvo com sucesso!")

# - O modelo treinado é salvo em um arquivo `.pkl` usando o módulo `pickle`.
# - Isso permite que o modelo seja carregado posteriormente para inferência sem precisar treiná-lo novamente.