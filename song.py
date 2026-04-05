class Song:
    def __init__(self, title, artist, total_plays):
        self.title = title
        self.artist = artist
        self.total_plays = total_plays

    def __repr__(self):
        return f"{self.title} by {self.artist}"