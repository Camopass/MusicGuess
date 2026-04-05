import json

class Song:
    def __init__(self, 
                 title, 
                 artist, 
                 total_plays,
                 correct_player,
                 incorrect_players,
                 album_art):
        self.title = title
        self.artist = artist
        self.total_plays = total_plays
        self.correct_player = correct_player
        self.incorrect_players = incorrect_players
        self.album_art = album_art

    @staticmethod
    def from_json(json: dict):
        return Song(json["title"],
                    json["artist"],
                    json["playcount"],
                    json["correct_player"],
                    json["incorrect_players"],
                    json["album_art"])
    
    @property
    def json_message(self) -> bytes:
        data = {
            "type": "song",
            "title": self.title,
            "artist": self.artist,
            "playcount": self.total_plays,
            "correct_player": self.correct_player,
            "incorrect_players": self.incorrect_players,
            "album_art": self.album_art
        }
        return json.dumps(data).encode("utf-8")
    

    def __repr__(self): 
        return f"{self.title} by {self.artist}"