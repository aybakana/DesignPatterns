"""
Prototype Design Pattern

This pattern creates new objects by cloning an existing object, known as the prototype.
Example demonstrates a document template cloning system.
"""
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, Any


class DocumentPrototype(ABC):
    """Abstract Prototype"""
    @abstractmethod
    def clone(self):
        pass


class Document(DocumentPrototype):
    """Concrete Prototype"""
    def __init__(self, content: Dict[str, Any]):
        self.content = content

    def clone(self) -> 'Document':
        # Using deepcopy to create a true copy of nested structures
        return Document(deepcopy(self.content))

    def get_content(self) -> Dict[str, Any]:
        return self.content

    def modify_content(self, key: str, value: Any):
        self.content[key] = value


class DocumentRegistry:
    """Prototype Registry"""
    def __init__(self):
        self._templates: Dict[str, Document] = {}

    def add_template(self, name: str, document: Document):
        self._templates[name] = document

    def get_template(self, name: str) -> Document:
        template = self._templates.get(name)
        if template:
            return template.clone()
        raise ValueError(f"Template '{name}' not found")


# Example usage
def main():
    # Create document registry
    registry = DocumentRegistry()

    # Create and register invoice template
    invoice_template = Document({
        'type': 'Invoice',
        'company': 'ACME Corp',
        'logo': 'acme_logo.png',
        'footer': 'Thank you for your business!',
        'fields': ['Item', 'Quantity', 'Price', 'Total']
    })
    registry.add_template('invoice', invoice_template)

    # Create and register report template
    report_template = Document({
        'type': 'Report',
        'company': 'ACME Corp',
        'logo': 'acme_logo.png',
        'sections': ['Summary', 'Analysis', 'Conclusions'],
        'footer': 'Confidential'
    })
    registry.add_template('report', report_template)

    # Create new documents from templates
    invoice1 = registry.get_template('invoice')
    invoice1.modify_content('customer', 'John Doe')
    invoice1.modify_content('amount', 1500)

    invoice2 = registry.get_template('invoice')
    invoice2.modify_content('customer', 'Jane Smith')
    invoice2.modify_content('amount', 2500)

    report1 = registry.get_template('report')
    report1.modify_content('title', 'Q1 Performance Analysis')
    report1.modify_content('author', 'Business Analytics Team')

    # Show the results
    print("Invoice 1:", invoice1.get_content())
    print("\nInvoice 2:", invoice2.get_content())
    print("\nReport 1:", report1.get_content())

    # Demonstrate that original templates remain unchanged
    original_invoice = registry.get_template('invoice')
    print("\nOriginal Invoice Template:", original_invoice.get_content())


if __name__ == "__main__":
    main()
