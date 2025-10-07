import csv 
import json
import numpy as np
import pandas as pd
import os

from surprise import Dataset, Reader, KNNBaseline, SVDpp, NormalPredictor, dump
from collections import defaultdict

from src.data_collection.file.file_paths import FilePaths

filename = FilePaths.champion_info()
with open(filename, 'r') as f:
    champ_data = json.load(f)

# contains index of championId and name
id_champ_map = {}
champion_list = []
for i, c in enumerate(champ_data['data'].keys()):
    id_champ_map[int(champ_data['data'][c]['key'])] = {'champion': champ_data['data'][c]['id'], 'index': i}
    champion_list.append(champ_data['data'][c]['id'])

with open('../objects/champion_list.json', 'w', newline='') as f:
    json.dump(champion_list, f, indent=4)

# load mastery_data and only present top 5 for 10% of dataset
filename = '../../data/complete_mastery_info.json'
with open(filename, 'r') as f:
    data = json.load(f)

skipped = {}
ratings = [] # list of items
r = np.zeros((len(data.keys()), len(champion_list)))
percent = 0.9
user_pool = [] # users that we should make predictions for
for i, key in enumerate(data.keys()):
    used = [] # used champions
    if i > (len(data.keys())*percent):
        skipped[key] = []
    for j, entry in enumerate(data[key]):
        if j == 0:
            # sorted in descending order
            maximum = entry['championPoints']
        if i > (len(data.keys())*percent):
            if j + 1 > 14:
                user_pool.append(key)
                break
            if j + 1 > 7: # testing set where we look at users with only top 7 champions available with other ratings hidden from model
                skipped[key].append(id_champ_map[entry['championId']]['champion'])
            else:
                score = entry['championPoints']/maximum
                item = id_champ_map[entry['championId']]['champion']
                ratings.append([key, item, score])
                used.append(item)
        else:
            score = entry['championPoints']/maximum
            item = id_champ_map[entry['championId']]['champion']
            ratings.append([key, item, score])
            used.append(item)

    # set unknown champion IDs to zero
    for champ in champion_list:
        if champ not in used:
            ratings.append([key, champ, 0])

print(f'users: {i}')
print(f'ratings: {len(ratings)}')

with open('../objects/next7.json', 'w', newline='') as f:
    json.dump(skipped, f, indent=4)
with open('../../data/final_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(ratings)
    
with open('../objects/user_pool.json', 'w', newline='') as f:
    json.dump(user_pool, f, indent=4)

test_path = os.path.expanduser('../../data/final_data.csv')
file_path = test_path
reader = Reader(sep=',', rating_scale=(0,1))
data = Dataset.load_from_file(file_path, reader)

most_played = {}

with open(file_path, 'r') as f:
    reader_obj = csv.reader(f)
    cur_id = ''
    most = []
    for row in reader_obj: 
        user_id, champion, score = row
        if cur_id != user_id:
            if cur_id != '':
                most_played[cur_id] = most
                most = []
            cur_id = user_id
        most.append(champion)

with open('../objects/most_played.json', 'w', newline='') as f:
    json.dump(most_played, f, indent=4)

trainset = data.build_full_trainset()

mean_rating = {}
# train models
sim_options = {
    "name": "pearson_baseline",
    "user_based": False
}

algs = [KNNBaseline(sim_options=sim_options, k=25), SVDpp(n_factors=10), NormalPredictor()]
labels = ['KNN', 'SVD', 'Random']

for (alg, l) in zip(algs, labels):
    algo = alg
    algo.fit(trainset)
    file_name = os.path.expanduser("model/" + l)
    print(f'saving {l}...')
    dump.dump(file_name, algo=algo)
