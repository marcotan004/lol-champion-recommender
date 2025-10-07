import requests
from requests import Response

import constants


def get_users_in_division(division: str, tier: str, queue: str, page: int):
    """
    Gets users in a division from the Riot API.
    :param division: target division
    :param tier: target tier
    :param queue: target queue type
    :param page: query page
    :return: Response containing users in a division
    """
    url: str = 'https://na1.api.riotgames.com/'
    query: str = f'lol/league/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={constants.RIOT_API_KEY}'
    return requests.get(url + query)


def get_champion_mastery_info(user_id: str) -> Response:
    """
    Gets champion mastery info for a user from the Riot API.
    :param user_id: PUUID of user
    :return: Response containing user's champion mastery info
    """
    url: str = 'https://na1.api.riotgames.com/'
    query: str = f'lol/champion-mastery/v4/champion-masteries/by-puuid/{user_id}?api_key={constants.RIOT_API_KEY}'

    return requests.get(url + query)

def add_user_mastery_data_to_dictionary(user_id: str, user_map: dict) -> None:
    """
    Adds user's champion mastery data to dictionary.
    :param user_id: PUUID of user
    :param user_map: map containing user's champion mastery data
    :return:
    """
    mastery_keys: list = ['championPoints', 'championId']
    mastery_info: Response = get_champion_mastery_info(user_id)

    if mastery_info.status_code == 200:
        mastery_info: dict = mastery_info.json()
        user_map[user_id]: list = []
        for entry in mastery_info:
            cleaned: dict = {key: entry[key] for key in mastery_keys}
            user_map[user_id].append(cleaned)
    else:
        print(mastery_info.reason)
