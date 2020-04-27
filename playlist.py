import json
import os
import pickle
from pathlib import Path


class Playlist:
    """
    Class representing a playlist of songs. Unlike the song queue the playlist does not remove songs from the data
    structure after they are played. The playlist is also saved to a specific discord server, thereby making it
    persistent.
    """
    def __init__(self, name, created_by, spotify_uri):
        self.name = name
        self.created_by = created_by
        self.description = None
        self.duration = 0
        # Each song consists of a pair (song_title, song_url).
        self.songs = []

        self.folder = "playlists/"

        # Creating the playlists folder if it does not already exist.
        Path(self.folder).mkdir(parents=True, exist_ok=True)

        self.filepath = self.folder + self.name + ".pickle"

        # Creating the pickle file that will contain all information about the playlist.
        self.save_playlist()

    def save_playlist(self):
        with open(self.filepath, "wb") as f:
            pickle.dump(self, f)
