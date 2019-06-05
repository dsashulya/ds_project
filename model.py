import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.cluster import KMeans
import pickle 

edamtx = sparse.csr_matrix(pd.read_csv('eda_log.csv'))

kmeans = KMeans(n_clusters=50)
kmeans.fit_predict(edamtx)

with open('model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)