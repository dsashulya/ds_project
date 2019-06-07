#testing

from flask import Flask, request, render_template, redirect, flash, jsonify
import numpy as np # to turn IN into array
import pandas as pd
import json
import pickle

def SortFirst(val):
    return val[0]
model = pickle.load(open('model.pkl', 'rb'))
eda = pd.read_csv('eda_total.csv')
eda = eda.loc[:, ['Unnamed: 0', 'img', 'title', 'link', 'ingredients', 'time', 'clusters']]

eda_log = pd.read_csv('eda_log.csv')
with open("ingredients_total.json", "r") as file:
    ingredients = json.load(file)

with open("ingredients_total_reversed.json", "r") as file:
    ingredients_reversed = json.load(file)
cols = np.load('columns.npy')
new_data = pd.DataFrame(0, index=[0], columns=cols)
new_row = {'minutes' : 60,ingredients_reversed['Говяжья печень'] : 500, ingredients_reversed['Сметана'] : 500, ingredients_reversed['Лук'] : 500}
for key, value in new_row.items():
    new_data[str(key)] = np.log(value) if value else 0

prediction = model.predict(new_data)[0]
dist_sort = [] 
recipes = eda[eda.clusters == prediction]
print(recipes.shape)
index_df = recipes.loc[:, 'Unnamed: 0']
for i in range(0, recipes.shape[0]):
    index_ = index_df.iloc[i] 
    control = 0
    dist = 0
    for key in new_data:
        if key in new_row and eda_log.loc[:, key][index_] != 0:
            dist += abs(min(new_row[key] - eda_log.loc[:, key][index_], 0))
            control += 1
        else:
            dist +=  20 * eda_log.loc[:, key][index_]
    if control >= 1:
        print(dist, control)
        dist_sort += [(dist, i)] 
    else:
        print(dist, '0')
dist_sort.sort(key = SortFirst )
print(dist_sort)
recipes_top = [key for value, key in dist_sort]
recipes_top_ = recipes_top[0:6]
recipes_ = recipes.iloc[recipes_top_, :]
print(recipes_.loc[:,'title'])
recipes = recipes_.loc[:, ['img', 'title', 'link', 'ingredients', 'time']]
