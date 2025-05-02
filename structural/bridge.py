"""
Bridge Design Pattern

This pattern decouples an abstraction from its implementation so that the two can vary independently.
Example demonstrates a remote control system for different types of devices.
"""
from abc import ABC, abstractmethod


class Device(ABC):
    """Implementation interface"""
    def __init__(self):
        self._volume = 0
        self._power = False
        self._channel = 1

    @abstractmethod
    def get_name(self) -> str:
        pass

    def is_enabled(self) -> bool:
        return self._power

    def enable(self):
        self._power = True
        print(f"{self.get_name()}: Power ON")

    def disable(self):
        self._power = False
        print(f"{self.get_name()}: Power OFF")

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, volume: int):
        if 0 <= volume <= 100:
            self._volume = volume
            print(f"{self.get_name()}: Volume set to {volume}")

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int):
        self._channel = channel
        print(f"{self.get_name()}: Channel set to {channel}")


class TV(Device):
    """Concrete Implementation"""
    def get_name(self) -> str:
        return "TV"


class Radio(Device):
    """Concrete Implementation"""
    def get_name(self) -> str:
        return "Radio"


class RemoteControl:
    """Abstraction"""
    def __init__(self, device: Device):
        self._device = device

    def toggle_power(self):
        if self._device.is_enabled():
            self._device.disable()
        else:
            self._device.enable()

    def volume_up(self):
        current_volume = self._device.get_volume()
        self._device.set_volume(min(100, current_volume + 10))

    def volume_down(self):
        current_volume = self._device.get_volume()
        self._device.set_volume(max(0, current_volume - 10))

    def channel_up(self):
        current_channel = self._device.get_channel()
        self._device.set_channel(current_channel + 1)

    def channel_down(self):
        current_channel = self._device.get_channel()
        self._device.set_channel(max(1, current_channel - 1))


class AdvancedRemoteControl(RemoteControl):
    """Refined Abstraction"""
    def mute(self):
        self._device.set_volume(0)

    def favorite_channel(self, number: int):
        print(f"Switching to favorite channel {number}")
        self._device.set_channel(number)


def main():
    # Create devices
    tv = TV()
    radio = Radio()

    # Create remote controls
    tv_remote = RemoteControl(tv)
    radio_remote = AdvancedRemoteControl(radio)

    # Test TV with basic remote
    print("\nTesting TV with basic remote:")
    tv_remote.toggle_power()
    tv_remote.volume_up()
    tv_remote.channel_up()
    tv_remote.toggle_power()

    # Test Radio with advanced remote
    print("\nTesting Radio with advanced remote:")
    radio_remote.toggle_power()
    radio_remote.volume_up()
    radio_remote.volume_up()
    radio_remote.mute()
    radio_remote.favorite_channel(5)
    radio_remote.toggle_power()


if __name__ == "__main__":
    main()
