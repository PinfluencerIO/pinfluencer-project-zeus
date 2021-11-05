import json

from src.data_access_layer.data_manager import DataManager
from src.web.processors.feed import ProcessPublicFeed

results = ProcessPublicFeed(DataManager()).do_process({})
print(json.dumps(results.body, indent=4))