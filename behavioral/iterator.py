"""
Iterator Design Pattern

This pattern provides a way to access the elements of an aggregate object
sequentially without exposing its underlying representation.
Example demonstrates a custom playlist system with different iteration methods.
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class Song:
    """Basic song class"""
    def __init__(self, title: str, artist: str, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration  # Duration in seconds

    def __str__(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{self.title} by {self.artist} ({minutes}:{seconds:02d})"


class Iterator(ABC):
    """Abstract Iterator"""
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Optional[Song]:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


class Playlist:
    """Aggregate interface"""
    @abstractmethod
    def create_normal_iterator(self) -> Iterator:
        pass

    @abstractmethod
    def create_shuffle_iterator(self) -> Iterator:
        pass


class NormalIterator(Iterator):
    """Concrete Iterator that iterates in normal order"""
    def __init__(self, songs: List[Song]):
        self._songs = songs
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._songs)

    def next(self) -> Optional[Song]:
        if self.has_next():
            song = self._songs[self._position]
            self._position += 1
            return song
        return None

    def reset(self) -> None:
        self._position = 0


class ShuffleIterator(Iterator):
    """Concrete Iterator that iterates in random order"""
    def __init__(self, songs: List[Song]):
        import random
        self._songs = songs.copy()
        random.shuffle(self._songs)
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._songs)

    def next(self) -> Optional[Song]:
        if self.has_next():
            song = self._songs[self._position]
            self._position += 1
            return song
        return None

    def reset(self) -> None:
        import random
        random.shuffle(self._songs)
        self._position = 0


class MusicPlaylist(Playlist):
    """Concrete Aggregate"""
    def __init__(self, name: str):
        self.name = name
        self._songs: List[Song] = []

    def add_song(self, song: Song) -> None:
        self._songs.append(song)

    def create_normal_iterator(self) -> Iterator:
        return NormalIterator(self._songs)

    def create_shuffle_iterator(self) -> Iterator:
        return ShuffleIterator(self._songs)


def play_playlist(name: str, iterator: Iterator) -> None:
    """Client code that uses the iterator"""
    print(f"\nPlaying {name}:")
    while iterator.has_next():
        song = iterator.next()
        if song:
            print(f"▶ {song}")


def main():
    # Create a playlist
    my_playlist = MusicPlaylist("My Favorite Songs")

    # Add some songs
    my_playlist.add_song(Song("Bohemian Rhapsody", "Queen", 354))
    my_playlist.add_song(Song("Stairway to Heaven", "Led Zeppelin", 482))
    my_playlist.add_song(Song("Hotel California", "Eagles", 391))
    my_playlist.add_song(Song("Sweet Child O' Mine", "Guns N' Roses", 356))
    my_playlist.add_song(Song("November Rain", "Guns N' Roses", 537))

    # Create iterators
    normal_iterator = my_playlist.create_normal_iterator()
    shuffle_iterator = my_playlist.create_shuffle_iterator()

    # Play playlist in normal order
    play_playlist("Normal Order", normal_iterator)

    # Play playlist in shuffle order
    play_playlist("Shuffle Order", shuffle_iterator)

    # Reset and replay shuffle to demonstrate different order
    print("\nReshuffling and replaying:")
    shuffle_iterator.reset()
    play_playlist("Shuffle Order (Replayed)", shuffle_iterator)


if __name__ == "__main__":
    main()
