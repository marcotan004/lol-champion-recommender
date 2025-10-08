import csv 
import json
import numpy as np
import pandas as pd
import os

from surprise import Dataset, Reader, KNNBaseline, SVDpp, NormalPredictor, dump
from collections import defaultdict

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
