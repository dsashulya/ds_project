from sklearn.cluster import KMeans
from scipy import sparse
import pandas as pd
import matplotlib.pyplot as plt

reader = pd.read_csv("eda_log.csv", low_memory=False)

edacopy = pd.DataFrame(reader)
edacopy.drop(columns='Unnamed: 0', inplace = True)
edamtx = sparse.csr_matrix(edacopy)

d = []

#выбор оптимального количества кластеров методом "локтя" 
#for i in range(1, 1000, 20):
#    kmeans = KMeans(n_clusters=i)
#    kmeans.fit_predict(edamtx)
#    d_current = kmeans.inertia_
#    print(d_current)
#    d += [(i, d_current)]
#plt.plot([x for x, y in d],[y for x, y in d])
#plt.show()


#расчет оптимального распределения по кластерам(50 кластера)
kmeans = KMeans(n_clusters=50)
kmeans.fit_predict(edamtx)
print(kmeans.inertia_)
c = {i: 0 for i in range(50)}
for i in kmeans.labels_:
    c[i] += 1
total = 0
for i, v in c.items():
    total += v
    print(f'{i}: {v}')
print(total)
