import csv 
import json
import numpy as np
import pandas as pd
import os
import pprint

from surprise import Dataset, Reader, accuracy, KNNWithMeans, SVD, NormalPredictor
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

def recommendChampion(uid, champs_played, champion_list, algo, n=10, ignore=5):
    print(f'User ID: {uid}')
    pprint.pprint(champs_played[:ignore])
    print(f'Recommendations for {uid}')
    count = 0
    for rec in get_top_n(uid, algo, champion_list, champs_played, n=n, ignore=ignore):
        print(rec[0])

filename = '../data/champion.json'
with open(filename, 'r') as f:
    champ_data = json.load(f)

# contains index of championId and name
id_champ_map = {}
champion_list = []
for i, c in enumerate(champ_data['data'].keys()):
    id_champ_map[int(champ_data['data'][c]['key'])] = {'champion': champ_data['data'][c]['id'], 'index': i}
    champion_list.append(champ_data['data'][c]['id'])

output = {'KNN': '', 'SVD': '', 'Random': ''}
for key in output.keys():
    output[key] = {
        'top5': [],
        'top10': [],
        'top15': [],
    }

for skip in range(1, 10):
    print(output)
    # load mastery_data and remove nth ranked champion from 10% of set
    filename = '../data/complete_mastery_info.json'
    with open(filename, 'r') as f:
        data = json.load(f)

    skipped = {}
    ratings = [] # list of items
    r = np.zeros((len(data.keys()), len(champion_list)))
    percent = 0.9
    for i, key in enumerate(data.keys()):
        used = []
        if i > (len(data.keys())*percent):
            skipped[key] = []
        for j, entry in enumerate(data[key]):
            if j == 0:
                # sorted in descending order
                maximum = entry['championPoints']
            if i > (len(data.keys())*percent):
                if j + 1 > 9+skip:
                    continue
                if j + 1 > 4+skip:
                    item = id_champ_map[entry['championId']]['champion']
                    skipped[key].append(id_champ_map[entry['championId']]['champion']) # add key, item, and rank #
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
    with open('../data/surprise_data_test.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(ratings)
        
    with open('../data/surprise_data_omit.csv', 'w', newline='') as f:
        json.dump(skipped, f, indent=4)

    test_path = os.path.expanduser('../data/surprise_data_test.csv')
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
            
            if cur_id in skipped.keys() and champion != skipped[cur_id]:
                most.append(champion)

    trainset = data.build_full_trainset()

    mean_rating = {}

    for rating in trainset.all_ratings():
        __, iid, rate = rating
        iid = trainset.to_raw_iid(iid)
        if iid not in mean_rating.keys():
            mean_rating[iid] = {'score': rate, 'n': 1, 'mean': rate}
        else:
            mean_rating[iid]['score'] += rate
            mean_rating[iid]['n'] += 1
            mean_rating[iid]['mean'] = mean_rating[iid]['score']/mean_rating[iid]['n']

    sim_options = {
        "name": "pearson_baseline",
        "user_based": False
    }

    algs = [KNNWithMeans(sim_options=sim_options), SVD(), NormalPredictor()]
    labels = ['KNN', 'SVD', 'Random']

    for (alg, l) in zip(algs, labels):
        algo = alg
        algo.fit(trainset)

        inside = [0,0,0]
        tot = 0

        for user in skipped.keys():
            if user not in most_played.keys():
                continue
            
            top_n = get_top_n(user, algo, champion_list, most_played[user], n=15, ignore=skip+4)
            for i, item in enumerate(top_n[:15]):
                if item[0] in skipped[user]:
                    if i < 5: 
                        inside[0] += 1
                    if i < 10:
                        inside[1] += 1
                    if i < 15:
                        inside[2] += 1

            tot += 1
        
        output[l]['top5'].append(inside[0]/tot)
        output[l]['top10'].append(inside[1]/tot)
        output[l]['top15'].append(inside[2]/tot)

filename = '../data/test_data/all_vals_n_predicted_6_to_10_no_mean.json'
with open(filename, 'w') as f:
    json.dump(output, f, indent=4)
    