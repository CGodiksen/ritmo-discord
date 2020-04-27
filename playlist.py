import json
import os
from pathlib import Path


class Playlist:
    """
    Class representing a playlist of songs. Unlike the song queue the playlist does not remove songs from the data
    structure after they are played. The playlist is also saved to a specific discord server, thereby making it
    persistent.
    """
    def __init__(self, name=None, created_by=None):
        self.name = name
        self.created_by = created_by
        self.description = None
        self.duration = 0
        self.songs = []

        self.folder = "playlists/"

        # Creating the playlists folder if it does not already exist.
        Path(self.folder).mkdir(parents=True, exist_ok=True)

        self.filepath = self.folder + self.name + ".json"

        # Creating the json file that will contain all information about the playlist if we are creating a new playlist.
        if name is not None and not os.path.isfile(self.filepath):
            self.save_playlist()

    def __str__(self):
        return ""

    def load_playlist(self):
        pass

    def save_playlist(self):
        pass
