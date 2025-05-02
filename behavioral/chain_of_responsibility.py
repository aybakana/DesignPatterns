"""
Chain of Responsibility Design Pattern

This pattern passes requests along a chain of handlers. Upon receiving a request,
each handler decides either to process the request or to pass it to the next handler
in the chain. Example demonstrates a support ticket handling system.
"""
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional


class SupportLevel(Enum):
    """Support ticket levels"""
    TECHNICAL = auto()
    BILLING = auto()
    CUSTOMER_SERVICE = auto()


class SupportTicket:
    """Support ticket class"""
    def __init__(self, customer: str, issue: str, level: SupportLevel):
        self.customer = customer
        self.issue = issue
        self.level = level

    def __str__(self):
        return f"[{self.level.name}] {self.customer}: {self.issue}"


class TicketHandler(ABC):
    """Abstract handler"""
    def __init__(self):
        self._next_handler: Optional[TicketHandler] = None

    def set_next(self, handler: 'TicketHandler') -> 'TicketHandler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, ticket: SupportTicket) -> bool:
        pass


class TechnicalSupportHandler(TicketHandler):
    """Handler for technical issues"""
    def handle(self, ticket: SupportTicket) -> bool:
        if ticket.level == SupportLevel.TECHNICAL:
            print(f"Technical Support handling ticket: {ticket}")
            print("Troubleshooting technical issues...")
            return True
        
        if self._next_handler:
            return self._next_handler.handle(ticket)
        return False


class BillingSupportHandler(TicketHandler):
    """Handler for billing issues"""
    def handle(self, ticket: SupportTicket) -> bool:
        if ticket.level == SupportLevel.BILLING:
            print(f"Billing Support handling ticket: {ticket}")
            print("Processing billing inquiry...")
            return True
        
        if self._next_handler:
            return self._next_handler.handle(ticket)
        return False


class CustomerServiceHandler(TicketHandler):
    """Handler for general customer service issues"""
    def handle(self, ticket: SupportTicket) -> bool:
        if ticket.level == SupportLevel.CUSTOMER_SERVICE:
            print(f"Customer Service handling ticket: {ticket}")
            print("Addressing customer concerns...")
            return True
        
        if self._next_handler:
            return self._next_handler.handle(ticket)
        return False


def main():
    # Create handlers
    technical = TechnicalSupportHandler()
    billing = BillingSupportHandler()
    customer_service = CustomerServiceHandler()

    # Create the chain
    technical.set_next(billing).set_next(customer_service)

    # Create some support tickets
    tickets = [
        SupportTicket("John Doe", "Can't login to application", SupportLevel.TECHNICAL),
        SupportTicket("Jane Smith", "Wrong charge on bill", SupportLevel.BILLING),
        SupportTicket("Bob Johnson", "Need to update address", SupportLevel.CUSTOMER_SERVICE),
        SupportTicket("Alice Brown", "Service unavailable", SupportLevel.TECHNICAL)
    ]

    # Process tickets
    print("Processing support tickets:\n")
    for ticket in tickets:
        print("-" * 50)
        if not technical.handle(ticket):
            print(f"No handler available for ticket: {ticket}")
        print()


if __name__ == "__main__":
    main()
