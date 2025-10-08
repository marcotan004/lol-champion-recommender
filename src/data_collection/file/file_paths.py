import os


class FilePaths:
    @staticmethod
    def data_directory() -> str:
        """
        Returns the path to the data directory.
        :return:
        """
        dir_path = os.path.dirname(__file__)
        data_directory = os.path.join(dir_path, '../../../data')
        data_directory = os.path.abspath(data_directory)
        if not (os.path.exists(data_directory)):
            os.makedirs(data_directory)

        return data_directory

    @staticmethod
    def champion_info() -> str:
        """
        Returns the path to the json containing the mapping of champion data to champion id.
        :return:
        """
        return os.path.join(FilePaths.champion_directory(), 'champion.json')

    @staticmethod
    def champion_directory() -> str:
        """
        Returns the path to the directory containing champion data.
        :return:
        """
        path = os.path.join(FilePaths.data_directory(), 'champion')
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def mastery_directory() -> str:
        """
        Returns the path to the directory containing mastery data.
        :return:
        """
        path = os.path.join(FilePaths.data_directory(), 'mastery')
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def output_directory() -> str:
        path = os.path.join(FilePaths.data_directory(), 'output')
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def skipped_users_file() -> str:
        """
        :return: filepath to skipped users data
        """
        return os.path.join(FilePaths.output_directory(), 'next_7.json')

    @staticmethod
    def ratings_data_file() -> str:
        """
        :return: filepath to ratings data
        """
        return os.path.join(FilePaths.output_directory(), 'ratings_data.csv')

    @staticmethod
    def training_user_ids_file() -> str:
        """
        :return: training user IDs filepath
        """
        return os.path.join(FilePaths.output_directory(), 'training_user_ids.json')

    @staticmethod
    def most_played_champions_per_user_file() -> str:
        """
        :return: most played champions per user file
        """
        return os.path.join(FilePaths.output_directory(), 'most_played_champions_per_user.json')