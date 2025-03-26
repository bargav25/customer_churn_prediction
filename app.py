from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from config.paths_config import MODEL_OUTPUT_PATH

app = Flask(__name__)

# Load the trained model
model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        data = request.form
        
        # Create a DataFrame with the input data
        input_data = pd.DataFrame({
            'Total_Trans_Amt': [float(data['Total_Trans_Amt'])],
            'Total_Trans_Ct': [float(data['Total_Trans_Ct'])],
            'Total_Ct_Chng_Q4_Q1': [float(data['Total_Ct_Chng_Q4_Q1'])],
            'Total_Revolving_Bal': [float(data['Total_Revolving_Bal'])],
            'Avg_Utilization_Ratio': [float(data['Avg_Utilization_Ratio'])],
            'Total_Relationship_Count': [float(data['Total_Relationship_Count'])],
            'Total_Amt_Chng_Q4_Q1': [float(data['Total_Amt_Chng_Q4_Q1'])],
            'Credit_Limit': [float(data['Credit_Limit'])],
            'Customer_Age': [float(data['Customer_Age'])],
            'Marital_Status': [float(data['Marital_Status'])]
        })
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'probability': float(probability[1]),
            'message': 'Customer will churn' if prediction == 1 else 'Customer will stay'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 