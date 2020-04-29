"""
Module with functions related to retrieving playlist information from spotify. For more information on the spotify
objects used in this module visit https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/.
"""
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyPlaylist:
    def __init__(self, playlist_uri):
        with open("config.json", "r") as config:
            config_dict = json.load(config)
            self.sp = spotipy.Spotify(client_credentials_manager=
                                      SpotifyClientCredentials(client_id=config_dict["spotify client id"],
                                                               client_secret=config_dict["spotify client secret"]))
        self.playlist = self.sp.playlist(playlist_uri)

    def get_name(self):
        """Returns the name of the playlist."""
        return self.playlist["name"]

    def get_description(self):
        """Returns the description of the playlist."""
        return self.playlist["description"]

    def get_artists_songs(self):
        """
        Extracts every song from the playlist together with the list of artists that made the song.

        :return: A string containing the song and every artist that is featured on the song. We return a string since
        we want to use it as a search query on youtube.
        """
        artists_songs = []

        # Iterating through the playlist track objects inside the paging object.
        for playlist_track in self.playlist["tracks"]["items"]:
            # Getting the track itself from the playlist track object.
            track = playlist_track["track"]

            # Extracting the list of artists and track name and creating the corresponding string.
            artists_song_str = ", ".join([artists["name"] for artists in track["artists"]]) + " - " + track["name"]

            artists_songs.append(artists_song_str)

        return artists_songs


spotify = SpotifyPlaylist("spotify:playlist:37i9dQZEVXcOvNUJbJEQ8Q")
print(spotify.get_name())
print(spotify.get_description())
print(spotify.get_artists_songs())
