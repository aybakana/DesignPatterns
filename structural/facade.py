"""
Facade Design Pattern

This pattern provides a unified interface to a set of interfaces in a subsystem.
Example demonstrates a home theater system with multiple components.
"""


class DVDPlayer:
    def __init__(self):
        self.movie = None

    def on(self):
        print("DVD Player: Powering on")

    def off(self):
        print("DVD Player: Powering off")

    def load(self, movie: str):
        self.movie = movie
        print(f"DVD Player: Loading '{movie}'")

    def play(self):
        if self.movie:
            print(f"DVD Player: Playing '{self.movie}'")
        else:
            print("DVD Player: No movie loaded")

    def stop(self):
        print("DVD Player: Stopping playback")

    def eject(self):
        if self.movie:
            print(f"DVD Player: Ejecting '{self.movie}'")
            self.movie = None
        else:
            print("DVD Player: No movie to eject")


class Amplifier:
    def on(self):
        print("Amplifier: Powering on")

    def off(self):
        print("Amplifier: Powering off")

    def set_volume(self, level: int):
        print(f"Amplifier: Setting volume to {level}")

    def set_surround_sound(self):
        print("Amplifier: Enabling surround sound")

    def set_stereo_sound(self):
        print("Amplifier: Enabling stereo sound")


class Projector:
    def on(self):
        print("Projector: Powering on")

    def off(self):
        print("Projector: Powering off")

    def wide_screen_mode(self):
        print("Projector: Switching to widescreen mode (16:9)")


class LightingSystem:
    def dim(self, level: int):
        print(f"Lighting: Dimming lights to {level}%")

    def brighten(self, level: int):
        print(f"Lighting: Brightening lights to {level}%")


class PopcornMaker:
    def on(self):
        print("Popcorn Maker: Powering on")

    def off(self):
        print("Popcorn Maker: Powering off")

    def pop(self):
        print("Popcorn Maker: Making popcorn")


class HomeTheaterFacade:
    """Facade for the home theater system"""
    def __init__(self):
        self.dvd = DVDPlayer()
        self.amp = Amplifier()
        self.projector = Projector()
        self.lights = LightingSystem()
        self.popcorn = PopcornMaker()

    def watch_movie(self, movie: str):
        print("\n=== Starting movie night ===")
        self.popcorn.on()
        self.popcorn.pop()
        self.lights.dim(20)
        self.projector.on()
        self.projector.wide_screen_mode()
        self.amp.on()
        self.amp.set_surround_sound()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.load(movie)
        self.dvd.play()

    def end_movie(self):
        print("\n=== Ending movie night ===")
        self.dvd.stop()
        self.dvd.eject()
        self.dvd.off()
        self.amp.off()
        self.projector.off()
        self.lights.brighten(100)
        self.popcorn.off()


def main():
    # Create the facade
    home_theater = HomeTheaterFacade()

    # Watch a movie
    home_theater.watch_movie("The Matrix")

    # End the movie
    home_theater.end_movie()


if __name__ == "__main__":
    main()
