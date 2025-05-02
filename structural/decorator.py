"""
Decorator Design Pattern

This pattern allows behavior to be added to individual objects dynamically.
Example demonstrates a text processing system with various formatting options.
"""
from abc import ABC, abstractmethod
from typing import Optional


class TextComponent(ABC):
    """Component interface"""
    @abstractmethod
    def get_text(self) -> str:
        pass


class PlainText(TextComponent):
    """Concrete component"""
    def __init__(self, text: str):
        self._text = text

    def get_text(self) -> str:
        return self._text


class TextDecorator(TextComponent):
    """Base decorator class"""
    def __init__(self, component: TextComponent):
        self._component = component

    def get_text(self) -> str:
        return self._component.get_text()


class BoldDecorator(TextDecorator):
    """Concrete decorator"""
    def get_text(self) -> str:
        return f"<b>{super().get_text()}</b>"


class ItalicDecorator(TextDecorator):
    """Concrete decorator"""
    def get_text(self) -> str:
        return f"<i>{super().get_text()}</i>"


class UnderlineDecorator(TextDecorator):
    """Concrete decorator"""
    def get_text(self) -> str:
        return f"<u>{super().get_text()}</u>"


class ColorDecorator(TextDecorator):
    """Concrete decorator"""
    def __init__(self, component: TextComponent, color: str):
        super().__init__(component)
        self._color = color

    def get_text(self) -> str:
        return f'<span style="color: {self._color}">{super().get_text()}</span>'


def main():
    # Create a simple text component
    text = PlainText("Hello, World!")
    print("\nOriginal text:", text.get_text())

    # Add bold formatting
    bold_text = BoldDecorator(text)
    print("Bold text:", bold_text.get_text())

    # Add italic formatting to bold text
    bold_italic_text = ItalicDecorator(bold_text)
    print("Bold and italic text:", bold_italic_text.get_text())

    # Create a new text with multiple decorators
    fancy_text = ColorDecorator(
        UnderlineDecorator(
            ItalicDecorator(
                PlainText("Fancy Text")
            )
        ),
        "blue"
    )
    print("Fancy text:", fancy_text.get_text())

    # Create a red bold text
    colored_bold_text = BoldDecorator(
        ColorDecorator(
            PlainText("Important Message"),
            "red"
        )
    )
    print("Colored bold text:", colored_bold_text.get_text())


if __name__ == "__main__":
    main()
