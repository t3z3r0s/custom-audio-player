from tkinter import filedialog
from pathlib import Path
import json

import cacheing

class PlaylistManager:

    MEDIAPLAYER_DIR = Path(__file__).parent.resolve()
    LOCAL_DIR = MEDIAPLAYER_DIR / "local"

    PLAYLIST_JSON_PATH = LOCAL_DIR / "playlists.json"


    def __init__(self):
        self.cached = cacheing.getPlaylistCache()
