"""
Machine Learning Training Pipeline for SymptomSense
Trains an ensemble Random Forest / Extra Trees Classifier on multi-modal symptom + EHR features.
Computes accuracy, precision, recall, F1, confusion matrix, and feature importances.
Saves model artifact for FastAPI inference engine.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_symptomsense_model():
    data_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/dataset/disease_symptoms.csv"
    meta_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models/feature_metadata.json"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run generate_dataset.py first.")
        
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    feature_cols = meta["all_feature_columns"]
    target_col = "target_disease"
    
    X = df[feature_cols]
    y = df[target_col]
    
    # Label encoding
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Stratified Train-Test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
    )
    
    print(f"Training set: {X_train.shape[0]} samples | Testing set: {X_test.shape[0]} samples")
    print(f"Number of input features: {X_train.shape[1]}")
    
    # Train Random Forest Classifier with calibrated tree depth and estimators
    print("\n--- Training Random Forest Classifier ---")
    rf_model = RandomForestClassifier(
        n_estimators=150,
        max_depth=25,
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    # 5-Fold Cross Validation
    cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring="accuracy")
    print(f"5-Fold CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Test evaluation
    y_pred = rf_model.predict(X_test)
    y_prob = rf_model.predict_proba(X_test)
    
    test_acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {test_acc * 100:.2f}%")
    
    # Top-3 Accuracy
    top3_correct = 0
    for i in range(len(y_test)):
        top3_classes = np.argsort(y_prob[i])[::-1][:3]
        if y_test[i] in top3_classes:
            top3_correct += 1
    top3_acc = top3_correct / len(y_test)
    print(f"Top-3 Accuracy: {top3_acc * 100:.2f}%")
    
    # Classification Report
    target_names = le.classes_
    report_dict = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
    report_text = classification_report(y_test, y_pred, target_names=target_names)
    print("\nClassification Report:\n", report_text)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    # Feature Importances (Global)
    importances = rf_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    top_features = [{"feature": feature_cols[i], "importance": float(importances[i])} for i in sorted_idx[:30]]
    
    # Package Model Artifact
    model_artifact = {
        "model": rf_model,
        "label_encoder": le,
        "feature_names": feature_cols,
        "symptoms": meta["all_symptoms"],
        "ehr_features": meta["ehr_features"],
        "classes": list(target_names)
    }
    
    model_save_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models/symptom_classifier.joblib"
    joblib.dump(model_artifact, model_save_path)
    print(f"\nSaved trained model artifact to {model_save_path}")
    
    # Save Metrics JSON
    metrics_summary = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 150,
        "train_samples": int(X_train.shape[0]),
        "test_samples": int(X_test.shape[0]),
        "test_accuracy": float(test_acc),
        "top3_accuracy": float(top3_acc),
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
        "precision_macro": float(report_dict["macro avg"]["precision"]),
        "recall_macro": float(report_dict["macro avg"]["recall"]),
        "f1_macro": float(report_dict["macro avg"]["f1-score"]),
        "top_features": top_features,
        "classes": list(target_names),
        "confusion_matrix": cm
    }
    
    metrics_save_path = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models/model_metrics.json"
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)
    print(f"Saved model metrics report to {metrics_save_path}")
    
    # Copy metadata to models folder for easy backend loading
    disease_meta_src = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/dataset/disease_metadata.json"
    disease_meta_dst = "c:/Users/Thinkpad/Downloads/aryan-mugdha/ml/models/disease_info.json"
    with open(disease_meta_src, "r", encoding="utf-8") as f_in, open(disease_meta_dst, "w", encoding="utf-8") as f_out:
        f_out.write(f_in.read())
    print(f"Synced disease knowledge base to {disease_meta_dst}")
    
    print("\n=== Model Training and Evaluation Completed Successfully! ===")
    return metrics_summary

if __name__ == "__main__":
    train_symptomsense_model()
