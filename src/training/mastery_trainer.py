import csv
import json
import numpy as np
import pandas as pd
import os

from surprise import Dataset, Reader, KNNBaseline, SVDpp, NormalPredictor, dump
from src.data_collection.file.file_paths import FilePaths


class MasteryTrainer:
    """
    MasteryTrainer trains mastery data on champion mastery data.
    """
    def __init__(self):
        """
        Initialize a new instance of the MasteryTrainer class.
        """
        self.ratings_path = FilePaths.ratings_data_file()
        self.sim_options = {"name": "pearson_baseline", "user_based": False}
        self.algorithms = [KNNBaseline(sim_options=self.sim_options, k=25), SVDpp(n_factors=10), NormalPredictor()]
        self.labels = ['KNN', 'SVD', 'Random']

    def train(self) -> None:
        """
        Train KNN models and save them to output directory.
        :return:
        """
        reader = Reader(sep=',', rating_scale=(0, 1))
        data = Dataset.load_from_file(self.ratings_path, reader)
        trainset = data.build_full_trainset()

        for (algorithm, label) in zip(self.algorithms, self.labels):
            algo = algorithm
            algo.fit(trainset)
            file_name = os.path.expanduser("model/" + label)
            print(f'saving {label}...')
            dump.dump(file_name, algo=algo)
