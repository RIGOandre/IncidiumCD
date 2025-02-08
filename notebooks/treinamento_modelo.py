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


df = pd.read_csv(r'C:\Users\manoa\Documents\GitHub\IncidiumCD\data\teste_indicium_precificacao.csv')


X = df.drop(columns=['price', 'id', 'host_id', 'host_name', 'nome', 'ultima_review'])
y = df['price']


numeric_features = ['latitude', 'longitude', 'minimo_noites', 'numero_de_reviews', 
                    'reviews_por_mes', 'calculado_host_listings_count', 'disponibilidade_365']
categorical_features = ['bairro_group', 'bairro', 'room_type']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  #  NaNs pela média
    ('scaler', StandardScaler())  # padronizar
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # substituir NaNs pela moda
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  #  one-Hot Encoding
])

# transformadores em um ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# pipeline completo (pré-processamento + modelo)
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# treino x teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# treinar modelo
model.fit(X_train, y_train)

# previsões no conjunto de teste
y_pred = model.predict(X_test)

# calcular RMSE manualmente
mse = mean_squared_error(y_test, y_pred) 
rmse = np.sqrt(mse)  

# exibir o RMSE
print(f'RMSE: {rmse}')

# salvar o modelo treinado em um arquivo .pkl
with open('../model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modelo treinado e salvo com sucesso!")