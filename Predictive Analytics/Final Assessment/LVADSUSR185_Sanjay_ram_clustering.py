# -*- coding: utf-8 -*-
"""FA_Clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yzWiZYEgMD3O4M7SZnqXt1emeBlnCc4F
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns

df = pd.read_csv("/content/customer_segmentation.csv")
df.head()

df.info()

df.isnull().sum()

#As there are only 24 null values among 2240 it is just 1% of the whole no of record so we can drop the na values
df.dropna(inplace=True)
df.isnull().sum()

df.duplicated().sum()

# Identify numerical columns by data type
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Create a box plot for each numerical column
for column in numerical_columns:
    plt.figure(figsize=(10, 6))  # Set the figure size for better readability
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(16, 10))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Heatmap of Correlation Matrix')
plt.show()

numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for i in range(len(numerical_columns)):
    for j in range(i + 1, len(numerical_columns)):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=numerical_columns[i], y=numerical_columns[j])
        plt.title(f'Scatter Plot between {numerical_columns[i]} and {numerical_columns[j]}')
        plt.show()

df.columns

df.info()

df.drop(columns=['ID','Year_Birth','Dt_Customer','AcceptedCmp2','AcceptedCmp3','AcceptedCmp4','AcceptedCmp5'],inplace=True)
df.head(5)

from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()
df['Education'] = label.fit_transform(df['Education'])
df['Marital_Status'] = label.fit_transform(df['Marital_Status'])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaled_df = df.copy()
scaler.fit(scaled_df)
scaled_df = scaler.transform(scaled_df)
scaled_df = pd.DataFrame(scaled_df)
scaled_df.columns = df.columns
print(scaled_df.head())

inertia_values = []
silhouette_scores = []
k_values = range(2, 10)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_df)
    inertia_values.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_df, kmeans.labels_))

plt.plot(k_values, inertia_values, marker='*',color='red')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Curve for determining Optimal k value')
plt.xticks(k_values)

optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(scaled_df)

cluster_labels = kmeans.predict(scaled_df)

silhouette_avg = silhouette_score(scaled_df, cluster_labels)
print("Ave silhouetter score: ",silhouette_avg)

scaled_df['cluster']=cluster_labels
print(kmeans.cluster_centers_)


df1 = scaled_df[scaled_df.cluster==0]
df2 = scaled_df[scaled_df.cluster==1]
df3 = scaled_df[scaled_df.cluster==2]
plt.scatter(df1['MntWines'],df1['MntFishProducts'],color='green')
plt.scatter(df2['MntWines'],df2['MntFishProducts'],color='red')
plt.scatter(df3['MntWines'],df3['MntFishProducts'],color='black')
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
plt.xlabel('MntWines')
plt.ylabel('MntFishProducts')
plt.legend()

df.columns

