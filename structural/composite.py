"""
Composite Design Pattern

This pattern composes objects into tree structures to represent part-whole hierarchies.
Example demonstrates a file system structure with files and directories.
"""
from abc import ABC, abstractmethod
from typing import List


class FileSystemComponent(ABC):
    """Component interface"""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def display(self, indent: str = "") -> None:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass


class File(FileSystemComponent):
    """Leaf class"""
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def display(self, indent: str = "") -> None:
        print(f"{indent}📄 {self.name} ({self._size} bytes)")

    def get_size(self) -> int:
        return self._size


class Directory(FileSystemComponent):
    """Composite class"""
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)

    def display(self, indent: str = "") -> None:
        print(f"{indent}📁 {self.name}/")
        for child in self._children:
            child.display(indent + "  ")

    def get_size(self) -> int:
        total_size = 0
        for child in self._children:
            total_size += child.get_size()
        return total_size


def main():
    # Create root directory
    root = Directory("root")

    # Create subdirectories
    documents = Directory("documents")
    pictures = Directory("pictures")

    # Create files
    file1 = File("document.txt", 100)
    file2 = File("document.pdf", 200)
    file3 = File("photo1.jpg", 500)
    file4 = File("photo2.jpg", 700)
    file5 = File("config.xml", 50)

    # Build directory structure
    documents.add(file1)
    documents.add(file2)

    pictures.add(file3)
    pictures.add(file4)

    root.add(documents)
    root.add(pictures)
    root.add(file5)

    # Display directory structure
    print("\nFile System Structure:")
    root.display()

    # Display sizes
    print(f"\nTotal size of root: {root.get_size()} bytes")
    print(f"Size of documents: {documents.get_size()} bytes")
    print(f"Size of pictures: {pictures.get_size()} bytes")


if __name__ == "__main__":
    main()
