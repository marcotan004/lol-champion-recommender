import csv
import json
import os
from collections import defaultdict

import numpy as np

from src.data_collection.file.file_paths import FilePaths
from src.data_collection.request.champion_loader import load_champion_json
from src.data_collection.request.mastery_loader import get_mastery_data


class MasteryDataLoader:
    def __init__(self, data_directory: str, percent: float = 0.9):
        self.TRAINING_CHAMPIONS_KEPT = 7
        self.TRAINING_CHAMPIONS_POOL = 7

        self.mastery_data = get_mastery_data(data_directory)
        self.percent = percent
        self.max_user_index = len(self.mastery_data.keys()) * self.percent
        self.missing_champions_for_training_users = defaultdict(list)
        self.champion_ratings = []
        self.training_user_ids = []
        self.id_to_champion = load_champion_json()
        self.champion_list = [self.id_to_champion[champ_id] for champ_id in self.id_to_champion]

    def add_missing_champions(self, user_id: str, seen_champions: set) -> None:
        """
        Adds missing champions to ratings list.
        :param user_id:
        :param seen_champions:
        :return:
        """
        # set unknown champion IDs to zero
        for champ in self.champion_list:
            if champ not in seen_champions:
                self.champion_ratings.append([user_id, champ, 0])

    def process_champion_mastery(self, user_id: int, mastery_entry: dict, maximum: float) -> None:
        """
        Add's champion mastery rating to the list of ratings.
        :param user_id:
        :param mastery_entry:
        :param maximum:
        :return:
        """
        score = mastery_entry['championPoints'] / maximum
        champion_name = self.id_to_champion[str(mastery_entry['championId'])]
        self.champion_ratings.append([user_id, champion_name, score])

    def process_user(self, user_index, user_id, user_mastery_data: dict) -> None:
        """
        Processes user data for training.
        :param user_index: index in list of user's mastery data
        :param user_id: associated user PUUID
        :param user_mastery_data: champion mastery data for a user
        :return:
        """
        maximum = user_mastery_data[0]['championPoints']
        seen_champions = set()
        is_training = user_index > (len(self.mastery_data.keys()) * self.percent)


        for nth_most_played, mastery_entry in enumerate(self.mastery_data[user_id]):
            champion_name = self.id_to_champion[str(mastery_entry['championId'])]

            if is_training and nth_most_played >= self.TRAINING_CHAMPIONS_KEPT:
                if nth_most_played >= self.TRAINING_CHAMPIONS_POOL + self.TRAINING_CHAMPIONS_KEPT:
                    self.training_user_ids.append(user_id)
                    return
                elif nth_most_played >= self.TRAINING_CHAMPIONS_KEPT:  # testing set where we look at users with only top 7 champions available with other ratings hidden from model
                    self.missing_champions_for_training_users[user_id].append(champion_name)
            else:
                self.process_champion_mastery(user_id, mastery_entry, maximum)
                seen_champions.add(champion_name)

        self.add_missing_champions(user_id, seen_champions)

    def create_data_set(self):
        r = np.zeros((len(self.mastery_data.keys()), len(self.champion_list)))

        for user_index, user_id in enumerate(self.mastery_data.keys()):
            self.process_user(user_index, user_id, self.mastery_data[user_id])

    def save_skipped_users(self):
        """
        Saves training user's next 7 champions to a file.
        :return:
        """
        with open(FilePaths.skipped_users_file(), 'w', newline='') as f:
            json.dump(self.missing_champions_for_training_users, f, indent=4)

    def save_ratings_data(self):
        """
        Saves ratings data to file.
        :return:
        """
        with open(FilePaths.ratings_data_file(), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.champion_ratings)

    def save_training_user_ids(self):
        """
        Save training user IDs to a file.
        :return:
        """
        with open(FilePaths.training_user_ids_file(), 'w', newline='') as f:
            json.dump(self.training_user_ids, f, indent=4)

    def save_all_data(self):
        """
        Save all data to respective files.
        :return:
        """
        self.save_skipped_users()
        self.save_ratings_data()
        self.save_training_user_ids()
