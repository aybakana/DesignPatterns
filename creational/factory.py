"""
Factory Design Pattern

This pattern provides an interface for creating objects but lets subclasses decide
which class to instantiate. Example demonstrates a payment method factory.
"""
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> None:
        pass


class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> None:
        print(f"Processing credit card payment of ${amount}")


class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> None:
        print(f"Processing PayPal payment of ${amount}")


class CryptoPayment(PaymentMethod):
    def process_payment(self, amount: float) -> None:
        print(f"Processing cryptocurrency payment of ${amount}")


class PaymentFactory:
    @staticmethod
    def create_payment(payment_type: str) -> PaymentMethod:
        if payment_type.lower() == "credit":
            return CreditCardPayment()
        elif payment_type.lower() == "paypal":
            return PayPalPayment()
        elif payment_type.lower() == "crypto":
            return CryptoPayment()
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")


# Example usage
def main():
    # Create a factory
    factory = PaymentFactory()
    
    # Create different payment methods
    credit_payment = factory.create_payment("credit")
    paypal_payment = factory.create_payment("paypal")
    crypto_payment = factory.create_payment("crypto")
    
    # Process payments
    credit_payment.process_payment(100.00)
    paypal_payment.process_payment(50.00)
    crypto_payment.process_payment(75.00)

if __name__ == "__main__":
    main()
