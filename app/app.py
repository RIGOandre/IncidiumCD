from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

with open('../model.pkl', 'rb') as f:
    model = pickle.load(f)

CSV_PATH = r"C:\Users\manoa\Documents\GitHub\IncidiumCD\data\teste_indicium_precificacao.csv"
data = pd.read_csv(CSV_PATH)
data['nome'] = data['nome'].fillna('').str.lower()
data = data.set_index('nome', drop=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower() 
    if not query:
        return jsonify([])

    results = data[data.index.str.startswith(query)]  
    results = results.to_dict(orient='records')
    return jsonify(results)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return jsonify({"prediction": f"${prediction[0]:.2f}"})

 
if __name__ == '__main__':
    app.run(debug=True)