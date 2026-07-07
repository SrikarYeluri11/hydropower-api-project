from flask import Flask , request, jsonify
import joblib
import pandas as pd


app= Flask(__name__)
API_KEY = "HYDROPOWER_CLIENT_2026"

model= joblib.load('linear_regression_model.pkl')
print('model loaded\n')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': ' HydroPower Prediction API is Running'
    })

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "Healthy"
    })

@app.route('/predict',methods=['POST'])
def predict():

    client_api_key= request.headers.get('x-api-key')

    if client_api_key != API_KEY:
        return jsonify({
            'Status': 'Failed',
            'Message': 'Invalid api key'
        }),401
    
    try:
        
        data= request.get_json()

        water_inflow= data['Water_Inflow']

        input_data= pd.DataFrame({
            'Water_Inflow': [water_inflow]
        })

        prediction = model.predict(input_data)

        return jsonify({
            'Water_Inflow': water_inflow,
            'Predicted_Power_Generated': round(float(prediction[0]),2) 
        })
    
    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 400
    
if __name__=='__main__':
    app.run(debug=True)

    