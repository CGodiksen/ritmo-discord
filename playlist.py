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
        # Each song consists of a pair (song_title, song_url).
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

    def load_playlist(self, name):
        """
        Loading attributes from the json file corresponding to the given playlist name into the object.

        :param name: The name of the playlist that we load into the object.
        """
        self.name = name

        if os.path.isfile(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)

        self.created_by = data["created by"]
        self.description = data["description"]
        self.duration = data["duration"]
        self.songs = data["songs"]

    def save_playlist(self):
        """Inserting object attributes into a dict and dumping the dict in the corresponding file."""
        data = {
            "name": self.name,
            "created by": self.created_by,
            "description": self.description,
            "duration": self.duration,
            "songs": self.songs,
        }

        with open(self.filepath, "w+") as f:
            json.dump(data, f)
