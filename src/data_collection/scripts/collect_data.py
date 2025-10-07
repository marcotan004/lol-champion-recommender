from src.data_collection.file.division_request_handler import DivisionRequestHandler
from src.data_collection.model.division import Division
from src.data_collection.model.tier import Tier

for division in Division:
    division_handler = DivisionRequestHandler(division.name, "GOLD", "RANKED_SOLO_5X5")
    division_handler.save_mastery_data()