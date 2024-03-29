"""A simple discord bot named Ritmo. Ritmo is a music bot that has expanded functionality through spotify integration.

The discord bot is implemented using a class based design with the "discord.Client" superclass from the
"discord" python package.
"""
import json
import discord
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
        """Displaying information about the bot and setting the activity when it is ready to run."""
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        # Setting the activity to "listening to !help" to make it easier for people to learn how Ritmo works.
        activity = discord.Activity(name='!help', type=discord.ActivityType.listening)
        await client.change_presence(activity=activity)

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

        if message.content.startswith("!shuffle"):
            self.song_queue.shuffle()

        if message.content.startswith("!queue"):
            await message.channel.send(str(self.song_queue))

        if message.content.startswith("!np"):
            await self.player.now_playing(message)

        if message.content.startswith("!create playlist"):
            SpotifyPlaylist(message.content[17:], message.guild.id)
            await message.add_reaction("\N{THUMBS UP SIGN}")

        if message.content.startswith("!delete playlist"):
            await self.delete_playlist(message)

        if message.content.startswith("!list playlists"):
            await self.display_playlists(message)

        if message.content.startswith("!info"):
            await self.display_playlist_info(message)

        if message.content.startswith("!tracklist"):
            await self.display_tracklist(message)

        if message.content.startswith("!help"):
            await self.display_help(message)

    async def play(self, message):
        """
        Adds the request to the queue and starts playing songs from the queue. If the request is the name of a saved
        playlist then we put every song from that playlist in the queue. Creates a player if there is none.
        """
        # Creating a player if there currently is none.
        if self.player is None:
            voice_channel = message.author.voice.channel
            self.player = await Player.create(voice_channel, self.user, self.song_queue)

        # Getting the playlist names for the specific server by finding the filenames and removing ".pickle".
        playlist_names = [playlist_name[:-7] for playlist_name in os.listdir("playlists/" + str(message.guild.id))]

        # If the content following "!play" is the name of a saved playlist then we push every song from the playlist.
        if message.content[6:] in playlist_names:
            playlist = await SpotifyPlaylist.load_playlist(message.content[6:], message.guild.id, message.channel)

            for song in playlist.tracklist:
                self.song_queue.push_song(song)
        else:
            # Appending the requested song to the song queue.
            self.song_queue.push_song(youtube.get_video_title_url(message.content[6:]))

        self.player.play()

    async def stop(self, message):
        """Stops the audio and disconnects the bot from the voice channel."""
        await self.player.stop(message)
        self.player = None

    @staticmethod
    async def delete_playlist(message):
        try:
            os.remove("playlists/" + str(message.guild.id) + "/" + message.content[17:] + ".pickle")
            await message.add_reaction("\N{THUMBS UP SIGN}")
        except FileNotFoundError:
            await message.channel.send("```There is no playlist with that name.```")

    @staticmethod
    async def display_tracklist(message):
        """
        Displays the tracklist of a playlist by sending 25 songs at a time. We are limited to 25 songs due to the
        character limit on discord messages.
        """
        playlist = await SpotifyPlaylist.load_playlist(message.content[11:], message.guild.id, message.channel)

        counter = 0
        while counter < len(playlist.tracklist):
            # Encapsulating the string representation in "```" to put the text in a code block in discord.
            playlist_str = "```"

            playlist_str += playlist.get_tracklist_str(counter, counter + 25)

            # Completing the code block encapsulation.
            playlist_str += "```"

            await message.channel.send(playlist_str)
            counter += 25

    @staticmethod
    async def display_playlists(message):
        """Displays the currently available playlists for the server."""
        # Encapsulating the string representation in "```" to put the text in a code block in discord.
        playlists_str = "```"

        # Getting the playlist names for the specific server by finding the filenames and removing ".pickle".
        playlist_names = [playlist_name[:-7] for playlist_name in os.listdir("playlists/" + str(message.guild.id))]

        # If the server has no playlists then we inform the user of that.
        if not playlist_names:
            await message.channel.send("```This server has no playlists.```")
            return

        for counter, playlist_name in enumerate(playlist_names):
            playlist = await SpotifyPlaylist.load_playlist(playlist_name, message.guild.id, message.channel)
            playlists_str += str(counter + 1) + ". " + playlist.get_info_str(verbose=False) + "\n"

        # Completing the code block encapsulation.
        playlists_str += "```"

        await message.channel.send(playlists_str)

    @staticmethod
    async def display_playlist_info(message):
        """Displays full information about a playlist."""
        # Encapsulating the string representation in "```" to put the text in a code block in discord.
        info_str = "```"

        playlist = await SpotifyPlaylist.load_playlist(message.content[6:], message.guild.id, message.channel)
        info_str += playlist.get_info_str()

        # Completing the code block encapsulation.
        info_str += "```"

        await message.channel.send(info_str)

    @staticmethod
    async def display_help(message):
        """Displays a help message that lists the available commands with accompanying explanations."""
        # Encapsulating the string representation in "```" to put the text in a code block in discord.
        help_str = "```"

        help_str += "!play *Song or Playlist* - Joins your voice channel and plays the song or playlist that " \
                    "you requested.\n\n"
        help_str += "!stop - Stops the music and leaves the voice channel.\n\n"
        help_str += "!pause - Pauses the music.\n\n"
        help_str += "!resume - Resumes the music.\n\n"
        help_str += "!skip - Skips the current song and continues to the next song in the queue.\n\n"
        help_str += "!shuffle - Shuffles the song queue.\n\n"
        help_str += "!queue - Displays the song queue.\n\n"
        help_str += "!np - Displays the currently playing song.\n\n"
        help_str += "!create playlist *Spotify playlist URI* - Creates a new playlist containing the songs from the" \
                    " given spotify playlist URI. To get the playlist URI, right-click a playlist on spotify -> Share" \
                    " -> Copy spotify URI.\n\n"
        help_str += "!delete playlist *Playlist name* - Deletes the playlist with the given name.\n\n"
        help_str += "!list playlists - Displays the list of available playlists.\n\n"
        help_str += "!info *Playlist name* - Displays information about the playlist with the given name.\n\n"
        help_str += "!tracklist *Playlist name* - Displays the tracklist of the playlist with the given name.\n\n"

        # Completing the code block encapsulation.
        help_str += "```"

        await message.channel.send(help_str)


if __name__ == '__main__':
    client = Ritmo()

    # Pulling the token from the config file and using it to set up the bot.
    with open("config.json", "r") as config:
        config_dict = json.load(config)
        client.run(config_dict["token"])
