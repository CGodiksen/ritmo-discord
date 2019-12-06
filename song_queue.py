class SongQueue:
    """Class representing a queue containing songs."""

    def __init__(self):
        self.queue = []

    def push_song(self, song):
        self.queue.append(song)

    def pop_song(self):
        return self.queue.pop(0)
