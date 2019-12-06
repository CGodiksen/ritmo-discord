"""A simple discord bot named Ritmo. Ritmo is a music bot that has expanded functionality through spotify integration.

The discord bot is implemented using a class based design with the "discord.Client" superclass from the
"discord" python package.
"""
import json
import discord
import song_queue
from bs4 import BeautifulSoup
import urllib.request


class Ritmo(discord.Client):
    """
    Class representing a discord bot object. The function "on_message" from the super class
    "discord.Clint" is overwritten to implement the functionality of the available commands.
    """

    def __init__(self, **options):
        self.queue = song_queue.SongQueue()
        super().__init__(**options)

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

        if message.content.starswith("!play ", 0, 6):
            self.queue.push_song(message.content[6:])

    async def play(self, song):
        pass

    def find_youtube_url(self, song):
        """
        Searches youtube using the song as the query and returns the first video url found.

        :param song: The song that we wish to find on youtube.
        :return: The url of the first video on the page when searching for the specified search query.
        """
        text_to_search = song

        query = urllib.parse.quote(text_to_search)
        url = "https://www.youtube.com/results?search_query=" + query

        response = urllib.request.urlopen(url)
        html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        return soup.find_next(attrs={'class': 'yt-uix-tile-link'})


client = Ritmo()

# Pulling the token from the config file and using it to set up the bot.
with open("config.json", "r") as config:
    config_dict = json.load(config)
    client.run(config_dict["token"])
