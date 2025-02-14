import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the dataset 
df = pd.read_csv('/kaggle/input/malicious-urls-dataset/malicious_phish.csv')

# Feature extraction function
def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_digits'] = len(re.findall(r'\d', url))
    features['num_special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
    features['num_subdomains'] = url.count('.') - 1  # Count subdomains
    features['has_https'] = 1 if url.startswith('https://') else 0
    features['has_www'] = 1 if 'www.' in url else 0
    return features

# Create a feature DataFrame
features = pd.DataFrame([extract_features(url) for url in df['url']])
features['label'] = df['type'].apply(lambda x: 1 if x == 'phishing' else 0)  # 1 for phishing, 0 for benign

# Split the dataset
X = features.drop('label', axis=1)
y = features['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an XGBoost Classifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

def predict_phishing(url):
    features = extract_features(url)
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)
    return "Phishing" if prediction[0] == 1 else "Benign"

# Example usage
url_to_check = "tinyurl.com"  # Replace with the URL you want to check
result = predict_phishing(url_to_check)
print(f"The URL '{url_to_check}' is classified as: {result}")
