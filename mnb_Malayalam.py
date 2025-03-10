# -*- coding: utf-8 -*-
"""MNB.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1o-APvgX40dsj_G_LV7cSu2F_zaR4464j
"""

from google.colab import drive

drive.mount('/content/gdrive', force_remount=True)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib
import random

train_data = pd.read_csv('/content/gdrive/MyDrive/Dravidian_Abusive/AWM_train_updated.csv')

vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(train_data['text'])
y_train = train_data['labels']

mnb_model = MultinomialNB()
mnb_model.fit(X_train_tfidf, y_train)

y_train_pred = mnb_model.predict(X_train_tfidf)

print("Classification Report:")
print(classification_report(y_train, y_train_pred))

accuracy = accuracy_score(y_train, y_train_pred)
print("Training Accuracy:", accuracy)

joblib.dump(mnb_model, '/content/gdrive/MyDrive/Dravidian_Abusive/AWMmnb_abusive_detector_model.pkl')
joblib.dump(vectorizer, '/content/gdrive/MyDrive/Dravidian_Abusive/AWMmnb_vectorizer.pkl')

new_comment = "നിങ്ങളെ ആരും ഇഷ്ടപ്പെടുന്നില്ലാ നിങ്ങളുടെ കാര്യം കേൾക്കുകയേ വേണ്ടാ നിങ്ങളെ വെറുത്തു പോയി. നിങ്ങൾ കാണിച്ച വഞ്ചനക്ക് നിങ്ങൾ ഒരു ദിവസ്സം അനുഭവിക്കും"
mnb_model = joblib.load('/content/gdrive/MyDrive/Dravidian_Abusive/AWMmnb_abusive_detector_model.pkl')
vectorizer = joblib.load('/content/gdrive/MyDrive/Dravidian_Abusive/AWMmnb_vectorizer.pkl')

new_vector = vectorizer.transform([new_comment])
prediction = mnb_model.predict(new_vector)

print("Prediction for new comment:", "Abusive" if prediction[0] == 1 else "Non-Abusive")

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


conf_matrix = confusion_matrix(y_train, y_train_pred)


disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['Non-Abusive', 'Abusive'])
disp.plot(cmap='Blues', values_format='d')
plt.title("Malayalam Confusion Matrix")
plt.show()

from sklearn.metrics import precision_recall_curve, average_precision_score


y_scores = mnb_model.predict_proba(X_train_tfidf)[:, 1]


precision, recall, thresholds = precision_recall_curve(y_train, y_scores)
avg_precision = average_precision_score(y_train, y_scores)

plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='b', label=f'Avg Precision = {avg_precision:.2f}')
plt.xlabel("Recall", fontsize=14)
plt.ylabel("Precision", fontsize=14)
plt.title("Malayalam Precision-Recall Curve", fontsize=16)
plt.legend(loc='upper right', fontsize=12)
plt.grid(alpha=0.3)
plt.show()

from sklearn.metrics import roc_curve, auc
e
fpr, tpr, _ = roc_curve(y_train, y_scores)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Guess')
plt.xlabel("False Positive Rate (FPR)", fontsize=14)
plt.ylabel("True Positive Rate (TPR)", fontsize=14)
plt.title("Malayalam AUC-ROC Curve", fontsize=16)
plt.legend(loc='lower right', fontsize=12)
plt.grid(alpha=0.3)
plt.show()

