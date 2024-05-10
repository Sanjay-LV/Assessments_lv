# -*- coding: utf-8 -*-
"""FA_Anomaly_detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VB1lxEFl2l79Us3MORqkiLJzkwK_-IZq
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/content/anomaly_train.csv")
df.head(10)

df.isnull().sum()

df.info()

df.describe()

df.duplicated(keep=False)

plt.figure(figsize=(16,9))
numerical_columns = df.select_dtypes(include=['int64','float64']).columns
sns.heatmap(data=df[numerical_columns].corr(),annot=True)

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

print(df.isnull().sum())

sns.countplot(x = df['Type'],palette='rainbow')

df.head(3)

label_encoder = LabelEncoder()
df['Type'] = label_encoder.fit_transform(df['Type'])
df['Location'] = label_encoder.fit_transform(df['Location'])

model_outlier = IsolationForest(contamination=0.1, random_state=42)
outliers = model_outlier.fit_predict(df[['Time','User','Amount']])
df['is_an_outlier'] = outliers

features = ['Time','User','Amount']
X = df[features]
y = df['is_an_outlier']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = IsolationForest(n_estimators=100, contamination=0.1, max_features=3, max_samples=10000, random_state=42)
model.fit(X_train)


y_pred = model.predict(X_train)
df["anomaly_score"] = model.decision_function(X)

anomalies = df.loc[df["anomaly_score"] < 0]

plt.scatter(df["User"], df["anomaly_score"], label="Not an Anomaly")
plt.scatter(anomalies["User"], anomalies["anomaly_score"], color="r", label="Anomaly")
plt.xlabel("User")
plt.ylabel("Anomaly Score")
plt.title("Scatter plot for User and Anomaly Score")
plt.legend(loc='lower right')
plt.show()

plt.scatter(df["Amount"], df["anomaly_score"], label="Not an Anomaly")
plt.scatter(anomalies["Amount"], anomalies["anomaly_score"], color="r", label="Anomaly")
plt.xlabel("Amount")
plt.ylabel("Anomaly Score")
plt.title("Scatter plot for Amount and Anomaly Score")
plt.legend(loc='lower right')
plt.show()

