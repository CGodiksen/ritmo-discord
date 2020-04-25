class SongQueue:
    """Class representing a queue containing songs."""

    def __init__(self):
        self.queue = []

    def push_song(self, song):
        self.queue.append(song)

    def pop_song(self):
        return self.queue.pop(0)

    def __str__(self):
        """String representation of the entire song queue."""
        # Encapsulating the string representation in "```" to put the text in a code block in discord.
        queue_str = "```Song queue:\n"

        # If there are any songs in the queue we list the song names in a numbered list.
        if self.queue:
            for counter, song in enumerate(self.queue):
                queue_str += str(counter + 1) + ". " + song[12:-4] + "\n"
        else:
            queue_str += "The queue is empty."

        # Completing the code block encapsulation.
        queue_str += "```"

        return queue_str
