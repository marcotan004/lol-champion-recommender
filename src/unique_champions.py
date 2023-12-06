import csv 
import json
import numpy as np
import pandas as pd
import os
import pprint
import random

from surprise import KNNWithMeans, SVD, NormalPredictor, dump
from collections import defaultdict

def get_top_n(uid, algo, champion_list, champs_played, n=10, ignore=5):
    top_n = defaultdict(list)
    for champ in champion_list:
        if champ not in champs_played[:ignore]:
            top_n[uid].append((champ,algo.predict(uid, champ).est))
            #top_n[uid].append((champ,algo.predict(uid, champ).est/mean_rating[iid]['mean']))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n[uid]

if __name__ == "__main__":
    # load user pool, most played list, and champion list
    with open('objects/champion_list.json', 'r') as f:
        champion_list = json.load(f)

    with open('objects/user_pool.json', 'r') as f:
        user_pool = json.load(f)
    
    with open('objects/most_played.json', 'r') as f:
        most_played = json.load(f)
    
    with open('objects/next7.json', 'r') as f:
        skipped = json.load(f)
    
    __, svd = dump.load('model/SVD')
    __, knn = dump.load('model/KNN')
    __, rands = dump.load('model/Random')

    test_IDS = []
    algs = [svd, knn, rands]
    labels = ['SVD', 'KNN', 'Random']
    unique = {'SVD': [], 'KNN': [], 'Random': []}
    
    for (alg, l) in zip(algs, labels):
        print(f'Algorithm {l}')
        for uid in user_pool:
            if uid in most_played.keys():
                for row in get_top_n(uid, alg, champion_list, most_played[uid], n=7, ignore=7):
                    unique[l].append(row[0])
        unique[l] = len(set(unique[l]))
    print(len(user_pool))
    print(unique)