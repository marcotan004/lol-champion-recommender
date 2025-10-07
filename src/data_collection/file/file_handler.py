import json
import os

def save_to_json(data: dict, file_path: str) -> None:
    """
    Saves data to a JSON file.
    :param data:
    :param file_path:
    :return:
    """
    dir_path: str = os.path.dirname(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def update_json(data: dict, file_name: str) -> None:
    """
    Updates JSON data in a file.
    :param data:
    :param file_name:
    :return:
    """
    with open(file_name, 'r+') as f:
        loaded_data = json.load(f)
        loaded_data.update(data)
        f.seek(0)
        json.dump(loaded_data, f, indent=4)
