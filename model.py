import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.cluster import KMeans
import pickle 

edamtx = pd.read_csv('eda_log.csv')
edamtx.drop(columns='Unnamed: 0', inplace=True)
edamtx = sparse.csr_matrix(edamtx)

kmeans = KMeans(n_clusters=50)
kmeans.fit_predict(edamtx)

with open('model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)
