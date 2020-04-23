import discord


class Player:
    """
    Class that handles functionality related to playing audio in a discord voice channel.
    """
    def __init__(self, voice_channel, user, song_queue):
        self.voice_channel = voice_channel
        self.user = user
        self.song_queue = song_queue

        # If the bot is not already in the voice channel we join the voice channel.
        if self.user not in voice_channel.members:
            self.voice_client = await voice_channel.connect()

    def play(self):
        """
        Iteratively plays every song in the song queue.

        :return: None
        """
        # If there are any songs in the queue we play the song that is first in the queue.
        if self.song_queue:
            # Recursively calls the Player.play function after the song is done to iterate through the queue.
            self.voice_client.play(discord.FFmpegPCMAudio(self.song_queue.pop_song()), after=self.play)
        # If the queue is empty we disconnect from the voice channel.
        else:
            self.voice_client.disconnect()
