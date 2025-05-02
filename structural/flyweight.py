"""
Flyweight Design Pattern

This pattern minimizes memory usage by sharing as much data as possible with similar objects.
Example demonstrates a character rendering system for a text editor.
"""
from typing import Dict


class CharacterStyle:
    """Flyweight class containing shared properties"""
    def __init__(self, font: str, size: int, bold: bool = False, italic: bool = False):
        self.font = font
        self.size = size
        self.bold = bold
        self.italic = italic

    def __repr__(self) -> str:
        style = []
        if self.bold:
            style.append("bold")
        if self.italic:
            style.append("italic")
        return f"CharacterStyle(font='{self.font}', size={self.size}, {' '.join(style)})"


class Character:
    """Context class containing extrinsic state"""
    def __init__(self, char: str, style: CharacterStyle, position_x: int, position_y: int):
        self.char = char
        self.style = style
        self.position_x = position_x
        self.position_y = position_y

    def render(self):
        style_desc = []
        if self.style.bold:
            style_desc.append("bold")
        if self.style.italic:
            style_desc.append("italic")
        style_str = f" ({', '.join(style_desc)})" if style_desc else ""
        
        print(f"Rendering '{self.char}' at position ({self.position_x}, {self.position_y}) "
              f"using {self.style.font} {self.style.size}pt{style_str}")


class StyleFactory:
    """Flyweight factory"""
    _styles: Dict[str, CharacterStyle] = {}

    @classmethod
    def get_style(cls, font: str, size: int, bold: bool = False, italic: bool = False) -> CharacterStyle:
        key = f"{font}-{size}-{bold}-{italic}"
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, bold, italic)
        return cls._styles[key]

    @classmethod
    def get_style_count(cls) -> int:
        return len(cls._styles)


class TextEditor:
    def __init__(self):
        self.characters: list[Character] = []

    def add_character(self, char: str, font: str, size: int, bold: bool, italic: bool, x: int, y: int):
        style = StyleFactory.get_style(font, size, bold, italic)
        character = Character(char, style, x, y)
        self.characters.append(character)

    def render_text(self):
        print("\nRendering text:")
        for char in self.characters:
            char.render()


def main():
    editor = TextEditor()

    # Add some text with different styles
    text = "Hello, World!"
    x = 0
    y = 0
    
    # Regular text
    for char in "Hello":
        editor.add_character(char, "Arial", 12, False, False, x, y)
        x += 10

    x += 10  # Add space
    
    # Bold text
    for char in "World":
        editor.add_character(char, "Arial", 12, True, False, x, y)
        x += 10

    # Add an exclamation mark in italic
    editor.add_character("!", "Arial", 12, False, True, x, y)

    # Render all text
    editor.render_text()

    # Show memory optimization
    print(f"\nTotal unique styles created: {StyleFactory.get_style_count()}")
    print("(Instead of creating a new style object for each character)")


if __name__ == "__main__":
    main()
