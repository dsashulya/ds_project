# преобразование данных к анализу
import pandas as pd

# считывание исходного файла
reader = pd.read_csv("edaru_main.csv")

ing = pd.DataFrame(reader)

ing_col = ing['ingredients']

# ручной словарь перевода склонения размерностей 
dict_name_ras = {'столовая ложка' : 'столовая ложка',
                 'столовые ложки' : 'столовая ложка',
                 'столовых ложек' : 'столовая ложка',
                 'столовой ложки' : 'столовая ложка',
                 'г' : 'г',
                 'кусок' : 'штука',
                 'куска' : 'штука',
                 'кусков' : 'штука',
                 'чайные ложки' : 'чайная ложка',
                 'чайная ложка' : 'чайная ложка',
                 'чайных ложек' : 'чайная ложка',
                 'чайной ложки' : 'чайная ложка',
                 'штук' : 'штука',
                 'штуки' : 'штука',
                 'штука' : 'штука',
                 'мл' : 'мл',
                 'стаканов' : 'стакан',
                 'стакана' : 'стакан',
                 'стакан' : 'стакан',
                 'кг' : 'кг',
                 'щепотка' : '1 г',
                 'банка' : 'банка',
                 'банки' : 'банка',
                 'л' : 'л',
                 'стебель' : 'штука',
                 'стеблей' : 'штука',
                 'стебля' : 'штука',
                 'пучок' : 'штука',
                 'пучка' : 'штука',
                 'пучков' : 'штука',
                 'головка' : 'головка',
                 'головки' : 'головка',
                 'головок' : 'головка',
                 'зубчик' : 'зубчик',
                 'зубчика' : 'зубчик',
                 'зубчиков' : 'зубчик',
                 'веточки' : 'штука',
                 'веточка' : 'штука',
                 'веточек' : 'штука',}

# размерности, которыми можно пренебречь 
pofig = ['вкусу', 'кончике ножа', '0']

nul = [0] * ing_col.shape[0]

dict_name_ing = {}

# перевод обычных дробей к десятичным
dict_amount = {'½' : '0.5',
                 '¼' : '0.25',
                 '⅔' : '0.67',
                 '¾' : '0.75',
                 '⅓' : '0.33'}

list_amount = ['½', '¼', '⅔', '¾', '⅓']

# перевод размерностей для гр или там, где нету ни граммов, ни мл(тупой, тк все штуки переводятся в фиксированное число граммов)
conversion_gr = {'г' : '1',
                 'мл' : '1',
                 'л' : '1000',
                 'столовая ложка' : '25',
                 'чайная ложка' : '10',
                 'стакан' : '200',
                 'кг' : '1000',
                 'щепотка' : '2',
                 'головка' : '20',
                 'зубчик' : '2',
                 'банка' : '300',
                 'штука' : '200'}

# перевод размерностей для мл(тупой, тк все штуки переводятся в фиксированное число мл)
conversion_ml = {'мл' : '1',
                 'л' : '1000',
                 'стакан' : '200',
                 'столовая ложка' : '20',
                 'чайная ложка' : '8',
                 'головка' : '20',
                 'зубчик' : '2',
                 'банка' : '300',
                 'штука' : '200'}

# приведение данных к виду: строки - блюда, столбцы - ингредиенты 
for num in range(0, ing_col.shape[0]):
    i = 0
    while(str(ing_col.iloc[num]).find(("name"), i) != -1):
        i = str(ing_col.iloc[num]).find(("name"), i) + 8
        st = ''
        while(str(ing_col.iloc[num])[i] != '"'):
            st += str(ing_col.iloc[num])[i]
            i += 1
        st_1 = ''
        i = str(ing_col.iloc[num]).find(("amount"), i) + 10
        while(str(ing_col.iloc[num])[i] != '"'):
            st_1 += str(ing_col.iloc[num])[i]
            i += 1
        if not(st in dict_name_ing):
            dict_name_ing[st] = 1
            ing[st] = nul
        ing.loc[num ,st] = st_1
        
# приведение данных внутри столбцов к единой размерности 
amount = []
for num in range(11, ing.shape[1]):
    kol = 0
    dict_ = {}
    for j in range(0, ing_col.shape[0]):
        st = str(ing.iloc[j, num]).split(' ')
        current = ''
        if (len(st) > 2):
            current = st[len(st) - 2] + ' ' + st[len(st) - 1]
        else:
            current = st[len(st) - 1]
        if (st[0] in list_amount):
           st[0] = dict_amount[st[0]]; 
        if not(current in pofig) and (current in dict_name_ras):
            if not(dict_name_ras[current] in dict_):
                dict_[dict_name_ras[current]] = 1
            if (len(st) > 2):
                del st[(len(st) - 2):len(st)]
                st += [dict_name_ras[current]]
            else:
                del st[(len(st) - 1):len(st)]
                st += [dict_name_ras[current]]
            if (len(st) > 1):
                kol += 1;
                ing.iloc[j, num] = st[0] + ' ' + st[1]
            else:
                ing.iloc[j, num] = st[0]
        else:
            if not(current in pofig):
                print(current)
        if (current in pofig):
            ing.iloc[j, num] = '0'
    amount += [(kol, num)]        
    for j in range(0, ing_col.shape[0]):
        st = str(ing.iloc[j, num]).split(' ')   
        if (len(st) > 1):
            current = ''
            if (len(st) > 2):
                current = st[len(st) - 2] + ' ' + st[len(st) - 1]
                del st[(len(st) - 2): len(st)]
            else:
                current = st[len(st) - 1]
                del st[(len(st) - 1): len(st)]
            st[0] = st[0].replace(',', '.')
            if ('мл' in dict_) and (current in conversion_ml) and not('г' in dict_):
                st[0] = str(float(conversion_ml[current]) * float(st[0]))
                st += ['мл']
                ing.iloc[j, num] = st[0] + ' ' + st[1]
            elif (current in conversion_gr):
                st[0] = str(float(conversion_gr[current]) * float(st[0]))
                st += ['г'] 
                ing.iloc[j, num] = st[0] + ' ' + st[1]
            else:
                ing.iloc[j, num] = st[0] + ' ' + current
    
    dict_ = {}
    for j in range(0, ing_col.shape[0]):
        st = str(ing.iloc[j, num]).split(' ')
        current = ''
        if (len(st) > 2):
            current = st[len(st) - 2] + ' ' + st[len(st) - 1]
        else:
            current = st[len(st) - 1] 
        if not(current in pofig) and not(current in dict_):
            dict_[current] = 1
        ing.iloc[j, num] = str(ing.iloc[j, num])
    print(list(dict_))

# сохранение приведенных данных 
ing.to_csv("edaru_main_up_1.csv")

# вывод топа популярных ингредиентов
amount.sort(reverse = True)
for i in range(0, 100):
    kol, name = amount[i]
    print(kol, list(ing.columns.values)[name])

