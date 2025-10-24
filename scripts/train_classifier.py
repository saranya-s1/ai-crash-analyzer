import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def train_classifier(data_csv, model_output_path):
    data = pd.read_csv(data_csv)
    texts = data['text']
    labels = data['label']

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    clf = LogisticRegression(max_iter=200)
    clf.fit(X, labels)

    # Save both model and vectorizer
    joblib.dump((vectorizer, clf), model_output_path)
    print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    data_csv = "history_learning/labeled_logs.csv"  # Your labeled dataset
    model_path = "ai_model/crash_classifier.joblib"
    if not os.path.exists(data_csv):
        print(f"[!] Training data file not found: {data_csv}")
    else:
        train_classifier(data_csv, model_path)
