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
        return os.path.join(FilePaths.data_directory(), 'champion')

    @staticmethod
    def mastery_directory():
        """
        Returns the path to the directory containing mastery data.
        :return:
        """
        return os.path.join(FilePaths.data_directory(), 'mastery')
