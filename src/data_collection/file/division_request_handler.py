import os
import time
import uuid

from requests import Response

from src.data_collection.file.file_handler import save_to_json
from src.data_collection.file.file_paths import FilePaths
from src.data_collection.request.riot import get_users_in_division, add_user_mastery_data_to_dictionary


class DivisionRequestHandler:
    """
    DivisionRequestHandler interacts with the Riot API to collect champion mastery data for users in a division.
    """
    def __init__(self, division, tier, queue):
        """
        Initialize a new instance of the DivisionRequestHandler class.
        :param division: Target division
        :param tier: Target tier
        :param queue: Target queue type
        """
        self.division = division
        self.tier = tier
        self.queue = queue

    def get_mastery_data_from_division_page(self, page: int, query_delay_in_seconds=1.35) -> dict:
        """
        Gets mastery data from a page within a division.
        :param page: the page within the division query
        :param query_delay_in_seconds: the delay between queries
        :return: map of champion mastery data of users within a division
        """
        player_list: Response = get_users_in_division(self.division, self.tier, 'RANKED_SOLO_5x5', page)
        player_list_json: dict = player_list.json()
        user_map = {}

        for i in range(len(player_list_json)):
            user_id = player_list_json[i]['puuid']
            add_user_mastery_data_to_dictionary(user_id, user_map)
            time.sleep(query_delay_in_seconds)

        return user_map

    def get_file_path(self) -> str:
        """
        Gets the file path for saving champion data in a page.
        :return: file path for champion data in a page
        """
        mastery_directory: str = FilePaths.mastery_directory()
        subdirectory: str = f'{self.tier}/{self.division}/{uuid.uuid4()}.json'
        return os.path.join(mastery_directory, subdirectory)

    def save_mastery_data(self) -> None:
        """
        Iterates through a division by page and saves mastery data in JSON format.
        :return:
        """
        number_of_pages: int = 300
        for page in range(1, number_of_pages):
            user_map: dict = self.get_mastery_data_from_division_page(page, query_delay_in_seconds=1.35)
            save_path: str = self.get_file_path()

            if not user_map:
                return

            save_to_json(user_map, save_path)