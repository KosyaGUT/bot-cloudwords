import json


with open('univer3.json', 'r', encoding='utf-8') as f:
    dict_list = json.load(f)  # Загружаем JSON файл как список словарей

# Объединяем все словари в один
univer_dict = {}
for d in dict_list:
    univer_dict.update(d)

