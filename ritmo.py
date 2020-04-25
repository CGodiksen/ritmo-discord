"""A simple discord bot named Ritmo. Ritmo is a music bot that has expanded functionality through spotify integration.

The discord bot is implemented using a class based design with the "discord.Client" superclass from the
"discord" python package.
"""
import json
import discord
import youtube

from song_queue import SongQueue
from player import Player


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
            await self.hello(message)

        if message.content.startswith("!play"):
            await self.play(message)

        if message.content.startswith("!stop"):
            await self.stop(message)

    @staticmethod
    async def hello(message):
        """Sends a message saying "Hi!"."""
        await message.channel.send("Hi!")

    async def play(self, message):
        """Adds the song to the queue and creates a player if there is none."""
        self.song_queue.push_song(youtube.get_youtube_video(message.content[6:], "audio_files/"))

        if self.player is None:
            voice_channel = message.author.voice.channel
            self.player = Player(voice_channel, self.user, self.song_queue)
            await self.player.play()

    async def stop(self, message):
        """Stops the audio and disconnects the bot from the voice channel."""
        # Only works if the message is from a user that is in the same voice channel as the bot.
        if self.player is not None and message.author.voice.channel.id == self.player.voice_channel.id:
            await self.player.stop()
            self.player = None


if __name__ == '__main__':
    client = Ritmo()

    # Pulling the token from the config file and using it to set up the bot.
    with open("config.json", "r") as config:
        config_dict = json.load(config)
        client.run(config_dict["token"])
