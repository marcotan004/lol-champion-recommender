from src.data_collection.file.file_paths import FilePaths
from src.training.mastery_data_loader import MasteryDataLoader

mastery_data_loader = MasteryDataLoader(FilePaths.mastery_directory(), 0.9)
mastery_data_loader.create_data_set()
mastery_data_loader.save_all_data()