from pathlib import Path
import json

import errorHandler

class cacheManager:

    CURRENT_WORKING_DIRECTORY = Path(__file__)
    CACHE_JSON_PATH = LOCAL_DIR / "cache.json"

    DEFAULT_CACHE = {
        "CURRENT_SONG": None,
        "CURRENT_PLAYLIST": None,
        "CURRENT_VOLUME" : None,
        "CURRENT_EQ" : None
    }



    def __init__(self):
        if not CACHE_JSON_PATH.is_file():
            try:
                with open("cache.json", "w") as f:
                json.dump(DEFAULT_CACHE, f, indent=4)

            except (FileNotFoundError, PermissionError, OSError) as e:
                errorHandler.cliErrorDisplay("Cache Retrieval Faliure", e)
                errorHandler.visualErrorDisplay("Cache Retrieval Faliure", e)
            


