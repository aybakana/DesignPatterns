"""
Strategy Design Pattern

This pattern defines a family of algorithms, encapsulates each one, and makes them
interchangeable. Example demonstrates a payment processing system with different
payment strategies.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from decimal import Decimal


@dataclass
class Item:
    """Simple item class"""
    name: str
    price: Decimal
    quantity: int

    @property
    def total(self) -> Decimal:
        return self.price * self.quantity


class PaymentStrategy(ABC):
    """Abstract Strategy"""
    @abstractmethod
    def pay(self, amount: Decimal) -> bool:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass


class CreditCardStrategy(PaymentStrategy):
    """Concrete Strategy for credit card payments"""
    def __init__(self, name: str, card_number: str, cvv: str, expiry_date: str):
        self._name = name
        self._card_number = card_number
        self._cvv = cvv
        self._expiry_date = expiry_date

    def pay(self, amount: Decimal) -> bool:
        if self.validate():
            print(f"Paid ${amount} using Credit Card ({self._card_number[-4:]})")
            return True
        return False

    def validate(self) -> bool:
        # Basic validation
        is_valid = (
            len(self._card_number) == 16 and
            len(self._cvv) == 3 and
            len(self._expiry_date) == 5  # MM/YY format
        )
        if not is_valid:
            print("Invalid credit card details")
        return is_valid


class PayPalStrategy(PaymentStrategy):
    """Concrete Strategy for PayPal payments"""
    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password

    def pay(self, amount: Decimal) -> bool:
        if self.validate():
            print(f"Paid ${amount} using PayPal account ({self._email})")
            return True
        return False

    def validate(self) -> bool:
        # Basic validation
        is_valid = (
            '@' in self._email and
            len(self._password) >= 8
        )
        if not is_valid:
            print("Invalid PayPal credentials")
        return is_valid


class CryptoStrategy(PaymentStrategy):
    """Concrete Strategy for cryptocurrency payments"""
    def __init__(self, wallet_address: str, crypto_type: str = "Bitcoin"):
        self._wallet_address = wallet_address
        self._crypto_type = crypto_type

    def pay(self, amount: Decimal) -> bool:
        if self.validate():
            print(f"Paid ${amount} equivalent using {self._crypto_type}")
            print(f"Sent to wallet: {self._wallet_address[:6]}...{self._wallet_address[-4:]}")
            return True
        return False

    def validate(self) -> bool:
        # Basic validation
        is_valid = len(self._wallet_address) >= 26
        if not is_valid:
            print("Invalid wallet address")
        return is_valid


class ShoppingCart:
    """Context class"""
    def __init__(self):
        self._items: List[Item] = []
        self._payment_strategy: Optional[PaymentStrategy] = None

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def remove_item(self, item: Item) -> None:
        self._items.remove(item)

    def get_total(self) -> Decimal:
        return sum(item.total for item in self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment_strategy = strategy

    def checkout(self) -> bool:
        if not self._items:
            print("Cart is empty")
            return False

        if not self._payment_strategy:
            print("Please select a payment method")
            return False

        total = self.get_total()
        print("\nCheckout Summary:")
        print("-" * 40)
        for item in self._items:
            print(f"{item.name} x{item.quantity}: ${item.total}")
        print("-" * 40)
        print(f"Total: ${total}")

        # Process payment
        if self._payment_strategy.pay(total):
            self._items.clear()
            return True
        return False


def main():
    # Create shopping cart
    cart = ShoppingCart()

    # Add items
    cart.add_item(Item("Python Book", Decimal("59.99"), 1))
    cart.add_item(Item("Mechanical Keyboard", Decimal("149.99"), 1))
    cart.add_item(Item("Coffee", Decimal("4.99"), 2))

    # Try checkout without payment strategy
    cart.checkout()

    # Checkout with credit card
    print("\nPaying with Credit Card:")
    credit_card = CreditCardStrategy(
        "John Doe",
        "1234567890123456",
        "123",
        "12/25"
    )
    cart.set_payment_strategy(credit_card)
    cart.checkout()

    # Add more items and checkout with PayPal
    cart.add_item(Item("Mouse Pad", Decimal("19.99"), 1))
    print("\nPaying with PayPal:")
    paypal = PayPalStrategy("john.doe@example.com", "secure_password")
    cart.set_payment_strategy(paypal)
    cart.checkout()

    # Try with invalid crypto wallet
    print("\nPaying with Crypto (Invalid):")
    crypto = CryptoStrategy("invalid_wallet")
    cart.set_payment_strategy(crypto)
    cart.checkout()

    # Pay with valid crypto wallet
    print("\nPaying with Crypto (Valid):")
    crypto = CryptoStrategy("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    cart.set_payment_strategy(crypto)
    cart.add_item(Item("USB Drive", Decimal("29.99"), 1))
    cart.checkout()


if __name__ == "__main__":
    main()
