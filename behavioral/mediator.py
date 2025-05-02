"""
Mediator Design Pattern

This pattern reduces coupling between components by having them communicate via a mediator object.
Example demonstrates a chat room system where users communicate through a mediator.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List


class ChatMediator(ABC):
    """Abstract Mediator"""
    @abstractmethod
    def send_message(self, message: str, user: 'User') -> None:
        pass

    @abstractmethod
    def add_user(self, user: 'User') -> None:
        pass

    @abstractmethod
    def remove_user(self, user: 'User') -> None:
        pass


class ChatRoom(ChatMediator):
    """Concrete Mediator"""
    def __init__(self, name: str):
        self.name = name
        self._users: List['User'] = []
        self._chat_history: List[str] = []

    def add_user(self, user: 'User') -> None:
        self._users.append(user)
        self._broadcast_message(f"SYSTEM: {user.name} has joined {self.name}")

    def remove_user(self, user: 'User') -> None:
        if user in self._users:
            self._users.remove(user)
            self._broadcast_message(f"SYSTEM: {user.name} has left {self.name}")

    def send_message(self, message: str, sender: 'User') -> None:
        if sender not in self._users:
            print(f"Error: {sender.name} is not in the chat room")
            return

        formatted_message = f"[{datetime.now().strftime('%H:%M:%S')}] {sender.name}: {message}"
        self._chat_history.append(formatted_message)
        self._broadcast_message(formatted_message, exclude_user=sender)

    def _broadcast_message(self, message: str, exclude_user: 'User' = None) -> None:
        for user in self._users:
            if user != exclude_user:
                user.receive_message(message)

    def show_history(self) -> None:
        print(f"\nChat History for {self.name}:")
        print("-" * 50)
        for message in self._chat_history:
            print(message)


class User:
    """Colleague class"""
    def __init__(self, name: str, privacy_mode: bool = False):
        self.name = name
        self._privacy_mode = privacy_mode
        self._chat_room: ChatMediator = None

    def join(self, chat_room: ChatMediator) -> None:
        if self._chat_room:
            self.leave()
        self._chat_room = chat_room
        chat_room.add_user(self)

    def leave(self) -> None:
        if self._chat_room:
            self._chat_room.remove_user(self)
            self._chat_room = None

    def send(self, message: str) -> None:
        if self._chat_room:
            self._chat_room.send_message(message, self)
        else:
            print(f"Error: {self.name} is not in any chat room")

    def receive_message(self, message: str) -> None:
        if self._privacy_mode:
            # In privacy mode, only show system messages and direct mentions
            if message.startswith("SYSTEM:") or self.name in message:
                print(f"[Private] {message}")
        else:
            print(message)


def main():
    # Create a chat room
    chat_room = ChatRoom("Python Developers")

    # Create users
    alice = User("Alice")
    bob = User("Bob")
    charlie = User("Charlie", privacy_mode=True)  # Charlie enables privacy mode
    david = User("David")

    # Users join the chat room
    alice.join(chat_room)
    bob.join(chat_room)
    charlie.join(chat_room)
    david.join(chat_room)

    # Simulate chat conversation
    alice.send("Hey everyone! Who's working on the new feature?")
    bob.send("I am! Need any help?")
    charlie.send("@Alice I can help too!")
    david.send("Count me in!")

    # Charlie leaves the chat
    charlie.leave()

    # More messages
    alice.send("Great! Let's coordinate on the implementation.")
    bob.send("Should we schedule a meeting?")

    # Show chat history
    chat_room.show_history()


if __name__ == "__main__":
    main()
