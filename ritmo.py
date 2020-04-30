"""A simple discord bot named Ritmo. Ritmo is a music bot that has expanded functionality through spotify integration.

The discord bot is implemented using a class based design with the "discord.Client" superclass from the
"discord" python package.
"""
import json
import discord
import pickle
import os
import youtube

from song_queue import SongQueue
from player import Player
from spotify_playlist import SpotifyPlaylist


class Ritmo(discord.Client):
    """
    Class representing a discord bot object. The function "on_message" from the super class
    "discord.Clint" is overwritten to implement the functionality of the available commands.
    """
    def __init__(self, **options):
        self.song_queue = SongQueue()
        super().__init__(**options)
        self.player = None

    async def on_ready(self):
        """Displaying information about the bot when it is ready to run."""
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        """
        This method is called every time a message is sent and if the message contains
        a command then that command is executed via another class method.
        """

        # Ignore if the message is from the bot itself.
        if message.author == self.user:
            return

        if message.content == "!hi":
            await message.channel.send("Hi!")

        if message.content.startswith("!play"):
            await self.play(message)

        if message.content.startswith("!stop"):
            if self.player is not None:
                await self.stop(message)

        if message.content.startswith("!pause"):
            if self.player is not None:
                self.player.pause()

        if message.content.startswith("!resume"):
            if self.player is not None:
                self.player.resume()

        if message.content.startswith("!skip"):
            if self.player is not None:
                self.player.skip()

        if message.content.startswith("!queue"):
            await message.channel.send(str(self.song_queue))

        if message.content.startswith("!np"):
            await self.player.now_playing(message)

        if message.content.startswith("!create playlist"):
            SpotifyPlaylist(message.content[17:])

        if message.content.startswith("!delete playlist"):
            os.remove("playlists/" + message.content[17:] + ".pickle")

        if message.content.startswith("!test"):
            with open("playlists/" + message.content[6:] + ".pickle", "rb") as f:
                playlist = pickle.load(f)

            print(playlist.name)

        if message.content.startswith("!info"):
            with open("playlists/" + message.content[6:] + ".pickle", "rb") as f:
                playlist = pickle.load(f)

            await message.channel.send(playlist.get_info())

    async def play(self, message):
        """Adds the song to the queue and starts playing songs from the queue. Creates a player if there is none."""
        # Creating a player if there currently is none.
        if self.player is None:
            voice_channel = message.author.voice.channel
            self.player = await Player.create(voice_channel, self.user, self.song_queue)

        # Appending the requested song to the song queue.
        self.song_queue.push_song(youtube.get_video_title_url(message.content[6:]))

        self.player.play()

    async def stop(self, message):
        """Stops the audio and disconnects the bot from the voice channel."""
        await self.player.stop(message)
        self.player = None


if __name__ == '__main__':
    client = Ritmo()

    # Pulling the token from the config file and using it to set up the bot.
    with open("config.json", "r") as config:
        config_dict = json.load(config)
        client.run(config_dict["token"])
