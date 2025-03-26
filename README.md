# Bank Customer Churn Prediction - MLOps Project

This project implements an end-to-end MLOps pipeline for predicting bank customer churn. It includes data ingestion, preprocessing, model training, and a web interface for predictions.

## 🚀 Features

- **Data Ingestion**: Automated data collection from Google Cloud Storage
- **Data Preprocessing**: 
  - Feature engineering
  - Handling categorical variables
  - Data balancing using SMOTE
  - Feature selection
- **Model Training**: 
  - LightGBM model with hyperparameter tuning
  - Model evaluation metrics
  - Model versioning with MLflow
- **Web Interface**: 
  - User-friendly Flask application
  - Real-time predictions
  - Interactive form with tooltips
  - Visual probability display

## 🛠️ Tech Stack

- **Python 3.11**
- **ML Libraries**:
  - scikit-learn
  - LightGBM
  - pandas
  - numpy
- **MLOps Tools**:
  - MLflow for experiment tracking
  - Google Cloud Storage for data storage
- **Web Framework**:
  - Flask
  - Bootstrap 5
- **Development Tools**:
  - joblib for model serialization
  - imbalanced-learn for handling class imbalance

## 📁 Project Structure

```
churn_pred/
├── artifacts/
│   ├── models/
│   │   └── model.pkl
│   ├── processed/
│   │   ├── train.csv
│   │   └── test.csv
│   └── raw/
│       ├── data.csv
│       ├── train.csv
│       └── test.csv
├── config/
│   ├── config.yaml
│   ├── model_params.py
│   └── paths_config.py
├── logs/
├── mlruns/
├── src/
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   └── model_training.py
├── templates/
│   └── index.html
├── utils/
│   └── common_functions.py
├── app.py
├── pipeline/
│   └── training_pipeline.py
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11
- Google Cloud Platform account (for data storage)
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd churn_pred
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google Cloud credentials:
   - Create a service account
   - Download the JSON key file
   - Set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

### Running the Pipeline

1. Train the model:
```bash
python pipeline/training_pipeline.py
```

2. Start the web application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## 📊 Model Features

The model uses the following features to predict customer churn:

1. **Customer Information**:
   - Customer Age
   - Marital Status

2. **Transaction Details**:
   - Total Transaction Amount
   - Total Transaction Count
   - Transaction Count Change (Q4 vs Q1)
   - Transaction Amount Change (Q4 vs Q1)

3. **Credit Information**:
   - Credit Limit
   - Total Revolving Balance
   - Average Utilization Ratio
   - Total Relationship Count

## 🎯 Model Performance

The LightGBM model achieves the following metrics:
- Accuracy: ~96%
- Precision: ~84%
- Recall: ~92%
- F1 Score: ~88%

## 🌐 Deployment

The application can be deployed on various platforms:

### Render (Recommended)
1. Push your code to GitHub
2. Create a Render account
3. Connect your GitHub repository
4. Deploy using the provided `render.yaml` configuration

### Other Options
- Heroku
- Python Anywhere
- Google Cloud Platform
- AWS Free Tier

## 📊 Dataset

The project uses the [Bank Customer Churn Prediction](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers) dataset from Kaggle. This dataset contains information about credit card customers and their churn behavior.




## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Bargav Jagatha** 

