"""
Module with functions related to retrieving playlist information from spotify.
"""
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials


with open("config.json", "r") as config:
    config_dict = json.load(config)
    sp = spotipy.Spotify(client_credentials_manager=
                         SpotifyClientCredentials(client_id=config_dict["spotify client id"],
                                                  client_secret=config_dict["spotify client secret"]))

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
