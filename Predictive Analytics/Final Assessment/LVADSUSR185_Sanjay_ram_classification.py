# -*- coding: utf-8 -*-
"""FA_Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ccsz9rQxQeTM4jDIY3H7LneIlZ9NixPH
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier as dcl
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
df = pd.read_csv("/content/penguins_classification.csv")
df.head()

df['species'].value_counts()

df.isnull().sum()

df.info()

df.describe()

# Plot histograms for numerical columns
for column in df.select_dtypes(include=['float64', 'int64']).columns:
    plt.figure(figsize=(10, 5))
    sns.histplot(df[column])
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

#As there are only 8null values among 274 values we can drop them
df.dropna(inplace=True)

df.isnull().sum()

for column in df.select_dtypes(include=['object']).columns:
    plt.figure(figsize=(10, 5))
    df[column].value_counts().plot(kind='bar')
    plt.title(f'Bar Chart of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.show()

numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for i in range(len(numerical_columns)):
    for j in range(i + 1, len(numerical_columns)):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=numerical_columns[i], y=numerical_columns[j])
        plt.title(f'Scatter Plot between {numerical_columns[i]} and {numerical_columns[j]}')
        plt.show()

# Create a box plot for each numerical column
for column in numerical_columns:
    plt.figure(figsize=(10, 6))  # Set the figure size for better readability
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()

Q1 = df['bill_length_mm'].quantile(0.25)
Q3 = df['bill_length_mm'].quantile(0.75)
IQR = Q3 - Q1
data = df[~((df['bill_length_mm'] < (Q1 - 1.5 * IQR)) | (df['bill_length_mm'] > (Q3 + 1.5 * IQR)))]

label_encoder = LabelEncoder()
df['species'] = label_encoder.fit_transform(df[['species']])
df['island'] = label_encoder.fit_transform(df[['island']])

df.head(5)

correlation_matrix = df.corr()
print(correlation_matrix)

df.info()

#Year is dropped since it has low correlation with the species column
X = df.drop(columns=['year','species'])
y = df['species']
scale = MinMaxScaler()
X_scale = pd.DataFrame(scale.fit_transform(X))
X_scale.columns = X.columns
X_train, X_test, y_train, y_test = train_test_split(X_scale, y, test_size=0.2, random_state=42)

model = dcl()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label=1)
recall = recall_score(y_test, y_pred, pos_label=1)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')

plt.title("Confusion Matrix")
sns.heatmap(conf_matrix,annot=True)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')

y_test.info()

