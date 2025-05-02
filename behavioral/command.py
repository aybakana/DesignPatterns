"""
Command Design Pattern

This pattern encapsulates a request as an object, thereby letting you parameterize
clients with different requests, queue or log requests, and support undoable operations.
Example demonstrates a smart home automation system with command history and undo capability.
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class Command(ABC):
    """Abstract command"""
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    """Receiver class"""
    def __init__(self, name: str):
        self.name = name
        self._is_on = False
        self._brightness = 0

    def turn_on(self) -> None:
        self._is_on = True
        print(f"{self.name} light is ON")

    def turn_off(self) -> None:
        self._is_on = False
        print(f"{self.name} light is OFF")

    def set_brightness(self, level: int) -> None:
        self._brightness = max(0, min(100, level))
        print(f"{self.name} light brightness set to {self._brightness}%")


class Thermostat:
    """Receiver class"""
    def __init__(self, name: str):
        self.name = name
        self._temperature = 20  # Default temperature in Celsius

    def set_temperature(self, temperature: float) -> None:
        self._temperature = temperature
        print(f"{self.name} thermostat set to {self._temperature}°C")


class LightOnCommand(Command):
    """Concrete command for turning light on"""
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_on()

    def undo(self) -> None:
        self._light.turn_off()


class LightOffCommand(Command):
    """Concrete command for turning light off"""
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_off()

    def undo(self) -> None:
        self._light.turn_on()


class SetThermostatCommand(Command):
    """Concrete command for setting thermostat"""
    def __init__(self, thermostat: Thermostat, temperature: float):
        self._thermostat = thermostat
        self._temperature = temperature
        self._previous_temperature: Optional[float] = None

    def execute(self) -> None:
        self._previous_temperature = self._thermostat._temperature
        self._thermostat.set_temperature(self._temperature)

    def undo(self) -> None:
        if self._previous_temperature is not None:
            self._thermostat.set_temperature(self._previous_temperature)


class SmartHomeAutomation:
    """Invoker class with command history"""
    def __init__(self):
        self._command_history: List[Command] = []
        self._undo_stack: List[Command] = []

    def execute_command(self, command: Command) -> None:
        command.execute()
        self._command_history.append(command)

    def undo_last_command(self) -> None:
        if not self._command_history:
            print("No commands to undo")
            return

        command = self._command_history.pop()
        command.undo()
        self._undo_stack.append(command)

    def show_history(self) -> None:
        print("\nCommand History:")
        for i, command in enumerate(self._command_history, 1):
            print(f"{i}. {command.__class__.__name__}")


def main():
    # Create receivers
    living_room_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    home_thermostat = Thermostat("Home")

    # Create commands
    living_room_on = LightOnCommand(living_room_light)
    living_room_off = LightOffCommand(living_room_light)
    bedroom_on = LightOnCommand(bedroom_light)
    set_thermostat = SetThermostatCommand(home_thermostat, 22.5)

    # Create invoker
    smart_home = SmartHomeAutomation()

    # Execute commands
    print("Executing commands:\n")
    smart_home.execute_command(living_room_on)
    smart_home.execute_command(bedroom_on)
    smart_home.execute_command(set_thermostat)
    
    # Show command history
    smart_home.show_history()

    # Undo last command
    print("\nUndo last command:")
    smart_home.undo_last_command()

    # Turn off living room light
    print("\nTurning off living room light:")
    smart_home.execute_command(living_room_off)

    # Show final history
    smart_home.show_history()


if __name__ == "__main__":
    main()
