from flask import Flask, request, render_template, redirect, flash, jsonify
import numpy as np # to turn IN into array
import pandas as pd
import json
import pickle

app = Flask(__name__)
app.secret_key = b'\x8e\xd761u\xf2\xcc?\xac<\xd7+a\xc1\xc5\x12'
model = pickle.load(open('model.pkl', 'rb'))

eda = pd.read_csv('eda_total.csv')
eda = eda.loc[:, ['img', 'title', 'link', 'ingredients', 'time', 'clusters']]

with open("ingredients_total.json", "r") as file:
    ingredients = json.load(file)

with open("ingredients_total_reversed.json", "r") as file:
    ingredients_reversed = json.load(file)

cols = np.load('columns.npy')

def chunks(l, n):
    """ yield successive chunks of size n from l """
    length = len(l)
    for i in range(0, length, n):
        yield l[i:i +n]

@app.route("/", methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        data = request.get_json()
        
        new_row = {}
        try:
            new_row['minutes'] = int(data['time'])
        except:
            return 'wrong time format'
        
        new_data = pd.DataFrame(0, index=[0], columns=cols)
        
        
        for i in range(len(data['ingredients'])):
            key = int(ingredients_reversed[data['ingredients'][i]])
            try:
                value = int(data['quantity'][i])
            except:
                continue
            if key not in new_row:
                new_row[key] = value
            else:
                new_row[key] += value
        
        for key, value in new_row.items():
            new_data[str(key)] = np.log(value) if value else 0
        
        
        prediction = model.predict(new_data)[0]
        
        recipes = eda[eda.clusters == prediction].sample(6)
        
        recipes = recipes.loc[:, ['img', 'title', 'link', 'ingredients', 'time']]
        recipes_json = []
        
        for img, title, link, ings, time in recipes.values:
            ings_list = []
            for i in eval(ings):
                ings_list.append(eval(i))
            
            recipes_json.append({
                'img': img if not pd.isnull(img) else "../static/noimage.png",
                'title': title,
                'link': link,
                'ings': ings_list,
                'time': time if not pd.isnull(time) else "-"
            })
        
        response = jsonify(recipes_json)
        
        # response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        

    recipes = eda.sample(6)
    recipes_json = []
    for img, title, link, ings, time, _ in recipes.values:
        ings_list = []
        for i in eval(ings):
            ings_list.append(eval(i))
        recipes_json.append({
            'img': img,
            'title': title,
            'link': link,
            'ings': ings_list,
            'time': time
        })
    
    return render_template('index.html', ingredients=ingredients,
                    recipes=recipes_json)
