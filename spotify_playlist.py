"""
Module with functions related to retrieving playlist information from spotify. For more information on the spotify
objects used in this module visit https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/.
"""
import spotipy
import json
import pickle
import pathlib
import youtube
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyPlaylist:
    def __init__(self, playlist_uri):
        # Getting the api client credentials from the config file and using them to set up a Spotify object.
        with open("config.json", "r") as config:
            config_dict = json.load(config)
            self.sp = spotipy.Spotify(client_credentials_manager=
                                      SpotifyClientCredentials(client_id=config_dict["spotify client id"],
                                                               client_secret=config_dict["spotify client secret"]))
        self.playlist = self.sp.playlist(playlist_uri)

        self.name = self.playlist["name"]
        self.description = self.playlist["description"]
        self.duration_ms = 0

        # Each song consists of a pair (song_title, song_url).
        self.tracklist = self.get_tracklist(self.get_search_queries())

        self.folder = "playlists/"

        # Creating the playlists folder if it does not already exist.
        pathlib.Path(self.folder).mkdir(parents=True, exist_ok=True)

        self.filepath = self.folder + self.name + ".pickle"
        self.save_playlist()

    def get_info_str(self, verbose=True):
        """
        Returns a prettified string containing information about the playlist.

        :param verbose: Bool that decides whether or not to add the description to the info string.
        """
        # Converting the duration from ms to hours and minutes.
        duration_mins = int((self.duration_ms / (1000 * 60)) % 60)
        duration_hours = int((self.duration_ms / (1000 * 60 * 60)) % 24)

        info = self.name + " - " + str(len(self.tracklist)) + " songs - " + str(duration_hours) + " hr " + \
               str(duration_mins) + " min"
        if verbose:
            info += "\n\n" + self.description

        return info

    def get_tracklist_str(self, start_index, end_index):
        """
        Creates a prettified string containing the songs from the start index to the end index.

        :param start_index: The index of the first song in the string.
        :param end_index: The index of the last song in the string.
        :return: The prettified string containing the songs from the start index to the end index.
        """
        songs_str = ""
        for counter, song in enumerate(self.tracklist[start_index:end_index]):
            songs_str += str(counter + start_index + 1) + ". " + song[0] + "\n"

        return songs_str

    def save_playlist(self):
        """Saving a pickle file that contains all information about the playlist."""
        with open(self.filepath, "wb") as f:
            pickle.dump(self, f)

    def get_search_queries(self):
        """
        Extracts every song from the playlist together with the list of artists that made the song to obtain high
        quality search queries that can be used to find the songs on youtube.

        :return: A string containing the song and every artist that made the song.
        """
        artists_songs = []

        # Iterating through the playlist track objects inside the paging object.
        for playlist_track in self.playlist["tracks"]["items"]:
            # Getting the track itself from the playlist track object.
            track = playlist_track["track"]

            # Extracting the list of artists and track name and creating the corresponding string.
            artists_song_str = ", ".join([artists["name"] for artists in track["artists"]]) + " - " + track["name"]

            artists_songs.append(artists_song_str)

            # Adding the duration of the track to the total duration of the playlist.
            self.duration_ms += track["duration_ms"]

        return artists_songs

    @staticmethod
    def get_tracklist(search_queries):
        """
        Searches for each song on youtube to find the URL of the song.

        :return: A list of tuples with the format: (song title, youtube URL).
        """
        return [youtube.get_video_title_url(search_query) for search_query in search_queries]

    @staticmethod
    def load_playlist(playlist_name):
        with open("playlists/" + playlist_name + ".pickle", "rb") as f:
            return pickle.load(f)
