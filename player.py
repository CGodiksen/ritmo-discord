import discord


class Player:
    """
    Class that handles functionality related to playing audio in a discord voice channel.
    """
    def __init__(self):
        self.voice_channel = None
        self.user = None
        self.song_queue = None
        self.voice_client = None

    @classmethod
    async def create(cls, voice_channel, user, song_queue):
        """
        Initializing the attributes of the Player object using the factory pattern.

        :param voice_channel: The voice channel that the person that typed the "!play" command is in.
        :param user: The user representing the bot itself.
        :param song_queue: The queue that contains the currently queued songs.
        :return: The fully initialized object.
        """
        self = Player()

        self.voice_channel = voice_channel
        self.user = user
        self.song_queue = song_queue

        self.voice_client = await self.voice_channel.connect()

        return self

    def play(self, error=None):
        """Iteratively plays every song in the song queue."""
        if error:
            raise Exception(str(error))

        if self.voice_client is not None:
            # If there are any songs in the queue we play the song that is first in the queue.
            if self.song_queue.queue:
                # Recursively calls the Player.play function after the song is done to iterate through the queue.
                self.voice_client.play(discord.FFmpegPCMAudio(source=self.song_queue.pop_song()), after=self.play)

    async def stop(self, message):
        """Stops the audio and disconnects the bot from the voice channel."""
        # Only works if the message is from a user that is in the same voice channel as the bot.
        if message.author.voice.channel.id == self.voice_channel.id:
            await self.voice_client.disconnect()

    def pause(self):
        """Pauses the audio playing if it is playing."""
        if self.voice_client.is_playing():
            self.voice_client.pause()

    def resume(self):
        """Resumes the audio playing if it is paused."""
        if self.voice_client.is_paused():
            self.voice_client.resume()

    def skip(self):
        """Skips the currently playing song."""
        self.voice_client.stop()
