import discord


class Player:
    """
    Class that handles functionality related to playing audio in a discord voice channel.
    """
    def __init__(self, voice_channel, user, song_queue):
        """
        Initializing the Player object with all needed attributes.

        :param voice_channel: The voice channel that the person that typed the "!play" command is in.
        :param user: The user representing the bot itself.
        :param song_queue: The queue that contains the currently queued songs.
        :return: None.
        """
        self.voice_channel = voice_channel
        self.user = user
        self.song_queue = song_queue

        self.voice_client = None

    async def play(self):
        """
        Iteratively plays every song in the song queue.

        :return: None
        """
        # If the bot is not already in the voice channel we join the voice channel.
        if self.user not in self.voice_channel.members:
            self.voice_client = await self.voice_channel.connect()

        # If there are any songs in the queue we play the song that is first in the queue.
        if self.song_queue:
            # Recursively calls the Player.play function after the song is done to iterate through the queue.
            self.voice_client.play(discord.FFmpegPCMAudio(self.song_queue.pop_song()))
        # If the queue is empty we disconnect from the voice channel.
        else:
            await self.voice_client.disconnect()

    async def stop(self):
        """Stops the audio and disconnects the bot from the voice channel."""
        self.voice_client.stop()
        await self.voice_client.disconnect()
