import csv 
import json
import numpy as np
import pandas as pd
import os
import pprint
import random

from surprise import KNNWithMeans, SVD, NormalPredictor, dump
from collections import defaultdict

import constants
from src.data_collection.file.file_paths import FilePaths


def get_top_n(uid, algo, champion_list, champs_played, n_recs=10, n_ignored=5):
    top_n = defaultdict(list)
    for champ in champion_list:
        if champ not in champs_played[:n_ignored]:
            top_n[uid].append((champ,algo.predict(uid, champ).est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n_recs]

    return top_n[uid]

def recommendChampion(uid, champs_played, champion_list, algo, skipped, n_recs=10, n_ignored=5):
    print(f'User ID: {uid}')
    print(f'Most played: {champs_played[:n_ignored]}')
    count = 0
    ret = []
    for rec in get_top_n(uid, algo, champion_list, champs_played, n_recs=n_recs, n_ignored=n_ignored):
        ret.append(rec[0])
    print(f'Recommended: {ret}')
    print(f'Actual: {skipped[uid]}') # the user's next 7 most played champions after recommended
    print(f'Overlap: {[x for x in ret if x in skipped[uid]]}')
    print()
    print()

if __name__ == "__main__":
    # load user pool, most played list, and champion list
    with open(FilePaths.champion_info(), 'r') as f:
        champion_info = json.load(f)
        champion_list = [champion_info[champ_id] for champ_id in champion_info]

    with open(FilePaths.training_user_ids_file(), 'r') as f:
        training_user_ids = json.load(f)
    
    with open(FilePaths.most_played_champions_per_user_file(), 'r') as f:
        most_played = json.load(f)
    
    with open(FilePaths.skipped_users_file(), 'r') as f:
        skipped = json.load(f)

    __, svd = dump.load(os.path.join(FilePaths.model_directory(), 'SVD'))
    __, knn = dump.load(os.path.join(FilePaths.model_directory(), 'KNN'))
    __, rands = dump.load(os.path.join(FilePaths.model_directory(), 'Random'))

    test_IDS = [random.choice(training_user_ids) for _ in range(constants.NUMBER_OF_TEST_USERS)]
    algorithms = [svd, knn, rands]
    labels = ['SVD', 'KNN', 'Random']

    for i in test_IDS:
        for (alg, l) in zip(algorithms, labels):
            print(f'Algorithm {l}')
            recommendChampion(i, most_played[i], champion_list, alg, skipped,
                              n_recs=constants.NUMBER_OF_RECOMMENDATIONS,
                              n_ignored=constants.TOP_N_IGNORED)