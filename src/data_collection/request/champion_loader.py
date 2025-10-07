import os

import requests
from requests import Response

from src.data_collection.file.file_handler import save_to_json
from src.data_collection.file.file_paths import FilePaths


def process_champion_json(request: Response) -> dict:
    """
    Processes champion JSON from DDragon and extracts required data.
    :param request:
    :return: Dictionary of needed champion data
    """
    json = request.json()
    saved_data = {int(json['data'][key]['key']): json['data'][key]['name'] for key in json['data']}
    return saved_data


def download_champion_json() -> None:
    """
    Downloads champion JSON from DDragon and saves required data.
    :return:
    """
    champion_json_link = "https://ddragon.leagueoflegends.com/cdn/15.20.1/data/en_US/champion.json"

    request = requests.get(champion_json_link)

    if request.status_code == 200:
        saved_data = process_champion_json(request)
        if not os.path.exists(FilePaths.champion_directory()):
            os.makedirs(FilePaths.champion_directory())
        save_to_json(saved_data, FilePaths.champion_info())
    else:
        print(request.reason)
