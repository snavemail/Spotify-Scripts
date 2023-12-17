class Song:
    def __init__(
        self,
        title: str,
        artist: str,
        explicit: bool,
        mins: int,
        seconds: int,
    ):
        self.title = title
        self.artist = artist
        self.explicit = explicit
        self.mins = mins
        self.seconds = seconds

    def __eq__(self, other):
        return (
            self.title == other.title
            and self.artist == other.artist
            and self.mins == other.mins
            and self.seconds == other.seconds
        )

    def __repr__(self):
        return f"{self.title} sung by {self.artist} is{' ' if self.explicit else ' not '}explicit and is {self.mins} minutes and {self.seconds} seconds long"
