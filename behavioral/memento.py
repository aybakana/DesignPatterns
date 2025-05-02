"""
Memento Design Pattern

This pattern lets you save and restore the previous state of an object without
revealing the details of its implementation. Example demonstrates a text editor
with undo/redo functionality.
"""
from datetime import datetime
from typing import List, Optional


class EditorMemento:
    """Memento class that stores editor state"""
    def __init__(self, content: str, cursor_position: int):
        self._content = content
        self._cursor_position = cursor_position
        self._saved_time = datetime.now()

    @property
    def content(self) -> str:
        return self._content

    @property
    def cursor_position(self) -> int:
        return self._cursor_position

    @property
    def saved_time(self) -> datetime:
        return self._saved_time


class TextEditor:
    """Originator class"""
    def __init__(self):
        self._content = ""
        self._cursor_position = 0

    def type(self, text: str) -> None:
        """Simulate typing text at cursor position"""
        before = self._content[:self._cursor_position]
        after = self._content[self._cursor_position:]
        self._content = before + text + after
        self._cursor_position += len(text)
        print(f"Typed: {text}")
        self._show_status()

    def delete(self, chars: int) -> None:
        """Delete specified number of characters before cursor"""
        if chars > self._cursor_position:
            chars = self._cursor_position

        before = self._content[:self._cursor_position - chars]
        after = self._content[self._cursor_position:]
        self._content = before + after
        self._cursor_position -= chars
        print(f"Deleted {chars} characters")
        self._show_status()

    def move_cursor(self, position: int) -> None:
        """Move cursor to specified position"""
        if 0 <= position <= len(self._content):
            self._cursor_position = position
            print(f"Moved cursor to position {position}")
            self._show_status()

    def _show_status(self) -> None:
        """Show current editor state"""
        print("\nCurrent text:", self._content)
        print("Cursor position:", self._cursor_position)
        print("Text before cursor:", self._content[:self._cursor_position])
        print("Text after cursor:", self._content[self._cursor_position:])
        print("-" * 50)

    def save(self) -> EditorMemento:
        """Create a memento of current state"""
        return EditorMemento(self._content, self._cursor_position)

    def restore(self, memento: EditorMemento) -> None:
        """Restore state from memento"""
        self._content = memento.content
        self._cursor_position = memento.cursor_position
        print("\nRestored to previous state:")
        self._show_status()


class History:
    """Caretaker class that manages editor history"""
    def __init__(self):
        self._history: List[EditorMemento] = []
        self._current_state = -1

    def push(self, memento: EditorMemento) -> None:
        """Add new state to history"""
        # Remove any states after current position (in case of new actions after undo)
        if self._current_state < len(self._history) - 1:
            self._history = self._history[:self._current_state + 1]
        
        self._history.append(memento)
        self._current_state = len(self._history) - 1
        print(f"Saved state at: {memento.saved_time}")

    def undo(self) -> Optional[EditorMemento]:
        """Get previous state"""
        if self._current_state > 0:
            self._current_state -= 1
            return self._history[self._current_state]
        return None

    def redo(self) -> Optional[EditorMemento]:
        """Get next state"""
        if self._current_state < len(self._history) - 1:
            self._current_state += 1
            return self._history[self._current_state]
        return None


def main():
    # Create editor and history
    editor = TextEditor()
    history = History()

    # Initial state
    history.push(editor.save())

    # Make some changes
    editor.type("Hello ")
    history.push(editor.save())

    editor.type("World!")
    history.push(editor.save())

    editor.move_cursor(5)
    editor.type("Beautiful ")
    history.push(editor.save())

    # Undo changes
    print("\nUndo last change:")
    memento = history.undo()
    if memento:
        editor.restore(memento)

    print("\nUndo one more time:")
    memento = history.undo()
    if memento:
        editor.restore(memento)

    # Redo changes
    print("\nRedo one change:")
    memento = history.redo()
    if memento:
        editor.restore(memento)

    # Make a new change after undo
    print("\nMaking new changes after undo:")
    editor.move_cursor(len(editor.save().content))
    editor.type(" How are you?")
    history.push(editor.save())


if __name__ == "__main__":
    main()
