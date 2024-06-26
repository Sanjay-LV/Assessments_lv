# -*- coding: utf-8 -*-
"""FA_Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pExTqj1iJpaugQQxuq6Iqi_MnZscbQMi
"""

import pandas as pd
import numpy as np
df = pd.read_csv("/content/Fare prediction.csv")
df.head()

df.isnull().sum()

df.info()

df.describe()

import matplotlib.pyplot as plt
import seaborn as sns
numerical_columns = df.select_dtypes(include=['int64','float64']).columns

# Create a box plot for each numerical column
for column in numerical_columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()

df.shape

df.drop(columns=['key'],inplace=True)
df.head(10)

df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

df['total_fare_amount'] = df['fare_amount']*df['passenger_count']
df.head()

df.info()

Q1 = np.quantile(df['total_fare_amount'],0.25)
Q3 = np.quantile(df['total_fare_amount'],0.75)

dis = Q3-Q1
lower_bound = Q1-1.5*dis
upper_bound = Q1+1.5*dis

df = df[~((df['total_fare_amount'] < lower_bound) | (df['total_fare_amount'] > upper_bound))]

plt.figure(figsize=(10, 5))
sns.histplot(df['total_fare_amount'])
plt.title('Histogram of fare_amount')
plt.xlabel('Fare_amount')
plt.ylabel('Frequency')
plt.show()

correlation_matrix = df.corr(numeric_only=True)
print(correlation_matrix)

from sklearn.preprocessing import MinMaxScaler
# As pickup longitude and pickup latitude has good correlation with dropoff we can drop 2 features among these 4
X = df.drop(columns=['fare_amount','pickup_datetime','pickup_longitude','dropoff_latitude'])
y = df['total_fare_amount']
scale = MinMaxScaler()
X_scale = pd.DataFrame(scale.fit_transform(X))
X_scale.columns = X.columns
X_scale.head(5)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
X_train, X_test, y_train, y_test = train_test_split(X_scale, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error

print(r2_score(y_pred,y_test))
print(mean_squared_error(y_test,y_pred))

