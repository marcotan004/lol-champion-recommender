import glob
import json
import os


def get_mastery_data(directory) -> dict:
    """
    Iterates through directory and loads all mastery data from it.
    :param directory: mastery data directory
    :return: dictionary of mastery data
    """
    mastery_data = {}
    directory = os.path.join(directory, '')

    for filename in glob.iglob(directory + '**/*.json', recursive=True):
        with open(filename, 'r') as f:
            data = json.load(f)
            mastery_data.update(data)

    return mastery_data