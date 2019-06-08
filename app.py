from flask import Flask, request, render_template, redirect, flash, jsonify
import numpy as np # to turn IN into array
import pandas as pd
import json
import pickle

app = Flask(__name__)
app.secret_key = b'\x8e\xd761u\xf2\xcc?\xac<\xd7+a\xc1\xc5\x12'
model = pickle.load(open('model.pkl', 'rb'))

eda = pd.read_csv('eda_total.csv')
eda = eda.loc[:, ['Unnamed: 0', 'img', 'title', 'link', 'ingredients', 'time', 'clusters']]

eda_log = pd.read_csv('eda_log.csv')
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
            portions = int(data['portions']) if int(data['portions']) else 1
        except:
            return 'wrong time or portions format'
        
        new_data = pd.DataFrame(0, index=[0], columns=cols)
        
        
        for i in range(len(data['ingredients'])):
            try:
                key = int(ingredients_reversed[data['ingredients'][i]])
            except KeyError:
                return 'ingredient not on the list'
            try:
                value = int(data['quantity'][i])
            except:
                continue
            if key not in new_row:
                new_row[str(key)] = value
            else:
                new_row[str(key)] += value
        
        for key, value in new_row.items():
            new_data[key] = np.log(value/portions) if value else 0
        print(new_row)
        
        prediction = model.predict(new_data)[0]
        print(prediction)
        dist_sort = [] 
        recipes = eda_log.iloc[eda[eda.clusters == prediction].index]

       
        for index, row in recipes.iterrows():
            dist = 0
            count = 0
            for ingredient in recipes.columns:
                if ingredient in new_row and row[ingredient] != 0:
                    dist += abs(min(np.log(new_row[ingredient] / portions ) - row[ingredient], 0))
                    count += 1
                else:
                    dist += 20 * row[ingredient]
            if count < 2:
                dist_sort += [(3000.0 + dist, index)]
            else:
                dist_sort += [(dist, index)]

        dist_sort.sort(key = lambda x: x[0])
        
        try:
            recipes_top = dist_sort[:6]
        except IndexError:
            recipes_top = dist_sort
        indexes = [x[1] for x in recipes_top]
        
        recipes__ = eda.loc[indexes, ['img', 'title', 'link', 'ingredients', 'time']]
        

        recipes_json = []
        for img, title, link, ings, time in recipes__.values:
            ings_list = []
            for i in eval(ings):
                ings_list.append(eval(i))
            
            recipes_json.append({
                'img': img if not pd.isnull(img) else "../static/noimage.png",
                'title': title if not pd.isnull(title) else "-",
                'link': link if not pd.isnull(link) else "#",
                'ings': ings_list if not pd.isnull(ings) else "-",
                'time': time if not pd.isnull(time) else "-"
            })
        
        response = jsonify(recipes_json)
        
        # response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        

    recipes = eda.sample(6)
    recipes_json = []
    for _, img, title, link, ings, time, _ in recipes.values:
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

if __name__ == '__main__':
    app.run()
