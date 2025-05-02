"""
Visitor Design Pattern

This pattern represents an operation to be performed on elements of an object structure.
It lets you define a new operation without changing the classes of the elements on which
it operates. Example demonstrates a document processing system.
"""
from abc import ABC, abstractmethod
from typing import List


class DocumentElement(ABC):
    """Element interface"""
    @abstractmethod
    def accept(self, visitor: 'DocumentVisitor') -> None:
        pass


class Document:
    """Object structure"""
    def __init__(self, title: str):
        self.title = title
        self.elements: List[DocumentElement] = []

    def add_element(self, element: DocumentElement) -> None:
        self.elements.append(element)

    def accept(self, visitor: 'DocumentVisitor') -> None:
        print(f"\nProcessing document: {self.title}")
        for element in self.elements:
            element.accept(visitor)


class TextElement(DocumentElement):
    """Concrete element"""
    def __init__(self, text: str):
        self.text = text

    def accept(self, visitor: 'DocumentVisitor') -> None:
        visitor.visit_text(self)


class ImageElement(DocumentElement):
    """Concrete element"""
    def __init__(self, source: str, caption: str = ""):
        self.source = source
        self.caption = caption

    def accept(self, visitor: 'DocumentVisitor') -> None:
        visitor.visit_image(self)


class TableElement(DocumentElement):
    """Concrete element"""
    def __init__(self, data: List[List[str]], headers: List[str] = None):
        self.data = data
        self.headers = headers or []

    def accept(self, visitor: 'DocumentVisitor') -> None:
        visitor.visit_table(self)


class DocumentVisitor(ABC):
    """Visitor interface"""
    @abstractmethod
    def visit_text(self, text: TextElement) -> None:
        pass

    @abstractmethod
    def visit_image(self, image: ImageElement) -> None:
        pass

    @abstractmethod
    def visit_table(self, table: TableElement) -> None:
        pass


class HTMLExportVisitor(DocumentVisitor):
    """Concrete visitor that exports to HTML"""
    def visit_text(self, text: TextElement) -> None:
        print(f"Converting text to HTML: <p>{text.text}</p>")

    def visit_image(self, image: ImageElement) -> None:
        caption = f'alt="{image.caption}"' if image.caption else ""
        print(f'Converting image to HTML: <img src="{image.source}" {caption}>')

    def visit_table(self, table: TableElement) -> None:
        print("Converting table to HTML:")
        html = ["<table>"]
        
        # Add headers if present
        if table.headers:
            header_row = "".join(f"<th>{h}</th>" for h in table.headers)
            html.append(f"<tr>{header_row}</tr>")
        
        # Add data rows
        for row in table.data:
            data_row = "".join(f"<td>{d}</td>" for d in row)
            html.append(f"<tr>{data_row}</tr>")
        
        html.append("</table>")
        print("\n".join(html))


class MarkdownExportVisitor(DocumentVisitor):
    """Concrete visitor that exports to Markdown"""
    def visit_text(self, text: TextElement) -> None:
        print(f"Converting text to Markdown: {text.text}")

    def visit_image(self, image: ImageElement) -> None:
        caption = f' "{image.caption}"' if image.caption else ""
        print(f'Converting image to Markdown: ![{image.caption}]({image.source}{caption})')

    def visit_table(self, table: TableElement) -> None:
        print("Converting table to Markdown:")
        
        # Print headers if present
        if table.headers:
            print(f"| {' | '.join(table.headers)} |")
            print(f"| {' | '.join(['---'] * len(table.headers))} |")
        
        # Print data rows
        for row in table.data:
            print(f"| {' | '.join(row)} |")


class StatisticsVisitor(DocumentVisitor):
    """Concrete visitor that gathers document statistics"""
    def __init__(self):
        self.text_count = 0
        self.total_words = 0
        self.image_count = 0
        self.table_count = 0
        self.total_cells = 0

    def visit_text(self, text: TextElement) -> None:
        self.text_count += 1
        self.total_words += len(text.text.split())

    def visit_image(self, image: ImageElement) -> None:
        self.image_count += 1

    def visit_table(self, table: TableElement) -> None:
        self.table_count += 1
        self.total_cells += sum(len(row) for row in table.data)

    def show_statistics(self) -> None:
        print("\nDocument Statistics:")
        print(f"Text elements: {self.text_count}")
        print(f"Total words: {self.total_words}")
        print(f"Images: {self.image_count}")
        print(f"Tables: {self.table_count}")
        print(f"Total table cells: {self.total_cells}")


def main():
    # Create a document
    doc = Document("Sample Document")

    # Add various elements
    doc.add_element(TextElement("Hello, this is a sample document."))
    doc.add_element(ImageElement("image.jpg", "Sample Image"))
    doc.add_element(TextElement("Here's a table showing some data:"))
    doc.add_element(TableElement(
        headers=["Name", "Age", "City"],
        data=[
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"]
        ]
    ))
    doc.add_element(ImageElement("chart.png", "Statistical Chart"))
    doc.add_element(TextElement("That's all folks!"))

    # Export to HTML
    print("=== HTML Export ===")
    html_visitor = HTMLExportVisitor()
    doc.accept(html_visitor)

    # Export to Markdown
    print("\n=== Markdown Export ===")
    markdown_visitor = MarkdownExportVisitor()
    doc.accept(markdown_visitor)

    # Gather statistics
    print("\n=== Document Statistics ===")
    stats_visitor = StatisticsVisitor()
    doc.accept(stats_visitor)
    stats_visitor.show_statistics()


if __name__ == "__main__":
    main()
