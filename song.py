class Song:
    def __init__(
        self,
        title: str,
        artist: str,
        album: str,
        explicit: bool,
        mins: int,
        seconds: int,
        date_added: int,
    ):
        self.title = title
        self.artist = artist
        self.album = album
        self.explicit = explicit
        self.mins = mins
        self.seconds = seconds
        self.date_added = date_added
