# -*- coding: utf-8 -*-
"""Predicitve_analytics_classification_IA2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EX2xOfM7xtdz4R9FzKT9J8uAFH73qvP9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("/content/winequality-red.csv")

df.head()

df.info()

df.describe()

df.isnull().sum()

df.duplicated().sum()
#treat duplicates
df = df.drop_duplicates()

df = df.dropna()

df.info()

numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

for column in numerical_columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()

# Calculate Q1, Q3, and IQR
q1 = np.percentile(df["pH"]	, 25)
q3 = np.percentile(df["pH"]	, 75)
iqr = q3 - q1

# Calculate outlier bounds
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Lower Bound (Outlier):", lower_bound)
print("Upper Bound (Outlier):", upper_bound)

def map_quality(quality):
    if quality >= 3 and quality <= 6:
        return 0
    elif quality >= 7 and quality <= 8:
        return 1
    else:
        return None

df['quality'] = df['quality'].apply(map_quality)

plt.figure(figsize=(8, 6))
sns.countplot(x='quality', data=df, palette='viridis')
plt.title('Wine Quality Distribution')
plt.xlabel('Quality')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()

X = df.drop(columns=['quality'])
y = df['quality']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

model.fit(X_train_resampled, y_train_resampled)

y_pred = model.predict(X_test)
#xgb_y_pred = xgb_classifier.predict(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print("Accuracy:", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall:", round(recall * 100, 2), "%")

# Generate a confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap="YlGnBu", fmt="d", cbar=False)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

