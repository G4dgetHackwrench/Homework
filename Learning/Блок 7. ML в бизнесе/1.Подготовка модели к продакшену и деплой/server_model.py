from flask import Flask, request, jsonify
import numpy as np
import pickle

with open('./data/model.pkl', 'rb') as pkl_file:
        model = pickle.load(pkl_file)
        
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    features = request.json
    features = np.array(features).reshape(1, 4)
    prediction = model.predict(features)
    return jsonify({
        'prediction':prediction[0]
    })
    
if __name__ == '__main__':
    app.run('localhost', 5000)