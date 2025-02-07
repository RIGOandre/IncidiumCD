from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

with open('../model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    
    df = pd.DataFrame([data])
    
    prediction = model.predict(df)
    return render_template('index.html', prediction=f"${prediction[0]:.2f}")

if __name__ == '__main__':
    app.run(debug=True)