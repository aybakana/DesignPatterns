"""
Abstract Factory Design Pattern

This pattern provides an interface for creating families of related or dependent
objects without specifying their concrete classes. Example demonstrates GUI elements
for different operating systems.
"""
from abc import ABC, abstractmethod


# Abstract Products
class Button(ABC):
    @abstractmethod
    def render(self):
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass


# Concrete Products for Windows
class WindowsButton(Button):
    def render(self):
        return "Rendering a Windows-style button"


class WindowsCheckbox(Checkbox):
    def render(self):
        return "Rendering a Windows-style checkbox"


# Concrete Products for macOS
class MacButton(Button):
    def render(self):
        return "Rendering a macOS-style button"


class MacCheckbox(Checkbox):
    def render(self):
        return "Rendering a macOS-style checkbox"


# Abstract Factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


# Concrete Factories
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


# Client code
class Application:
    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = None
        self.checkbox = None

    def create_ui(self):
        self.button = self.factory.create_button()
        self.checkbox = self.factory.create_checkbox()

    def render(self):
        print(self.button.render())
        print(self.checkbox.render())


# Example usage
def main():
    # Create Windows UI
    windows_factory = WindowsFactory()
    windows_app = Application(windows_factory)
    windows_app.create_ui()
    print("Windows UI:")
    windows_app.render()

    print("\n")

    # Create macOS UI
    mac_factory = MacFactory()
    mac_app = Application(mac_factory)
    mac_app.create_ui()
    print("macOS UI:")
    mac_app.render()


if __name__ == "__main__":
    main()
