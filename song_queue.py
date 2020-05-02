import youtube
import time
import os
import random


class SongQueue:
    """Class representing a queue containing songs."""

    def __init__(self):
        # Contains songs, each represented by a tuple consisting of the song title and song url.
        self.queue = []

        # We maintain a downloaded queue to keep track of the songs in the queue which are downloaded.
        # The purpose of this is to download songs before they are to be played to increase responsiveness.
        self.downloaded_queue = []

    def push_song(self, title_url):
        """
        Adding a song to the queue. Also downloading the song if needed.

        :param title_url: A tuple consisting of a song title and the youtube url to the song.
        :return: None
        """
        # Adding the song to the normal queue.
        self.queue.append(title_url)

        # If there are still two or less songs in the queue we download it and add the filename to the downloaded songs.
        if len(self.queue) <= 2:
            song_file = youtube.download_mp3(title_url[1], "audio_files/")
            self.downloaded_queue.append(song_file)

    def pop_song(self):
        """
        Removing the first song in the queue and popping the song filename from the downloaded queue.

        :return: The filename of the song that is first in the queue.
        """
        del self.queue[0]
        # If the queue contains songs but the downloaded queue is empty we know that we are currently downloading and we
        # therefore wait for the download to finish.
        while self.queue and not self.downloaded_queue:
            time.sleep(0.5)
        return self.downloaded_queue.pop(0)

    def update_downloaded_queue(self):
        """
        Updating the queue containing downloaded songs if there are any songs in the normal queue that are not
        downloaded yet.
        """
        if len(self.queue) >= 2:
            song_file = youtube.download_mp3(self.queue[1][1], "audio_files/")
            self.downloaded_queue.append(song_file)

    def shuffle(self):
        """Shuffles the song queue, randomizing the order of the songs."""
        shuffle_queue = self.queue
        self.queue = []

        # Removing the songs from the audio files folder that were next on the queue before the shuffle.
        for file in self.downloaded_queue:
            os.remove(file)

        # Shuffling the queue in place.
        random.shuffle(shuffle_queue)

        # Adding the songs back to the song queue.
        for song in shuffle_queue:
            self.push_song(song)

    def __str__(self):
        """String representation of the entire song queue."""
        # Encapsulating the string representation in "```" to put the text in a code block in discord.
        queue_str = "```Song queue (" + str(len(self.queue)) + " songs):\n"

        # If there are any songs in the queue we list the song names in a numbered list.
        if self.queue:
            for counter, song in enumerate(self.queue[:10]):
                queue_str += str(counter + 1) + ". " + song[0] + "\n"
            if len(self.queue) > 10:
                queue_str += "..."
        else:
            queue_str += "The queue is empty."

        # Completing the code block encapsulation.
        queue_str += "```"

        return queue_str
