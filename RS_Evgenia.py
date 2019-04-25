import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
# раскомментить для запуска
# приведение ячейки к единому типу float  
#reader = pd.read_csv("edaru_main_up_1.csv", low_memory=False)

#ing_df = pd.DataFrame(reader)

## end_up_rs
#for i in range(0, ing_df.shape[0]):
#    for j in range(11, ing_df.shape[1]):
#        st = str(ing_df.iloc[i , j]).split(' ')
#        ing_df.iloc[i, j] = float(st[0])

#ing_df.to_csv("edaru_main_up_rs.csv")

#удаление первых столбцов для блюд 
reader = pd.read_csv("edaru_breakfast_up_rs.csv", low_memory=False)

ing_df = pd.DataFrame(reader)

ind_drop_col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

top_ing = []

#возможное удаление топых ингредиентов может помочь при кластеризации 
with open('edaru_breakfast_top_100.txt', 'r') as file:
    top_ing += [line.split() for line in file]

for i in range(0, len(top_ing)):
    st = ''
    for j in range(1, len(top_ing[i])):
        st += str(top_ing[i][j])
        if j != len(top_ing[i]) - 1:
            st += ' '
    top_ing[i] = [top_ing[i][0], st]        

for ing_kol, ing_name in top_ing:
    if int(ing_kol) > 100:
        ind_drop_col += [ing_df.columns.get_loc(ing_name)]
    
ing_df.drop(ing_df.columns[ind_drop_col], axis=1,
            inplace=True)

#кластреризация
# 1 способ: метод к-средних или ближайших соседей

#model = KMeans()



#knn = KNeighborsClassifier()
#grid = GridSearchCV(knn, param_grid={'n_neighbors': n_neighbors_array})
#all_pr = model.predict(ing_df)

#print(all_pr[all_pr != 2])

# 2 способ: плотность

dbscan = DBSCAN(200, 1)

dbscan.fit(ing_df)

ans = []

dict_ = {}

for i in range(0, ing_df.shape[0]):
    ans += [dbscan.labels_[i]]
    if not(str(dbscan.labels_[i]) in dict_):
        dict_[str(dbscan.labels_[i])] = 0;
    dict_[str(dbscan.labels_[i])] += 1;
    
for i in dict_.keys():
    print(i, dict_[i])

#samples = ing_df.values

#mergings = linkage(samples, method = 'complete')

#dendrogram(mergings,
#           labels = ing_df,
#           leaf_rotation = 90,
#           leaf_font_size = 6)

#plt.show()
