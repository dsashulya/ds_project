import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.cluster import KMeans
import pickle 

eda = pd.read_csv('eda_log.csv')
eda.drop(columns='Unnamed: 0', inplace=True)

np.save('columns.npy', eda.columns)

eda = sparse.csr_matrix(eda)

kmeans = KMeans(n_clusters=50)
clusters = kmeans.fit_predict(eda)

eda = pd.read_csv('eda_total.csv')

eda['clusters'] = list(clusters)

eda.to_csv('eda_total.csv')

with open('model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)
