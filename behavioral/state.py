"""
State Design Pattern

This pattern allows an object to alter its behavior when its internal state changes.
Example demonstrates a vending machine with different states and transitions.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class VendingMachineState(ABC):
    """Abstract State"""
    @abstractmethod
    def insert_money(self, amount: int) -> None:
        pass

    @abstractmethod
    def select_product(self, product: str) -> None:
        pass

    @abstractmethod
    def dispense_product(self) -> None:
        pass

    @abstractmethod
    def refund(self) -> None:
        pass


class VendingMachine:
    """Context class"""
    def __init__(self):
        # Initialize states
        self._no_money_state = NoMoneyState(self)
        self._has_money_state = HasMoneyState(self)
        self._sold_state = SoldState(self)
        self._sold_out_state = SoldOutState(self)

        # Set initial state
        self._state = self._no_money_state
        
        # Initialize inventory and money
        self._inventory: Dict[str, Dict[str, any]] = {
            "A1": {"name": "Cola", "price": 2, "quantity": 5},
            "A2": {"name": "Chips", "price": 1, "quantity": 3},
            "A3": {"name": "Candy", "price": 1, "quantity": 10}
        }
        self._current_money = 0
        self._selected_product: Optional[str] = None

    def set_state(self, state: VendingMachineState) -> None:
        self._state = state

    def get_no_money_state(self) -> VendingMachineState:
        return self._no_money_state

    def get_has_money_state(self) -> VendingMachineState:
        return self._has_money_state

    def get_sold_state(self) -> VendingMachineState:
        return self._sold_state

    def get_sold_out_state(self) -> VendingMachineState:
        return self._sold_out_state

    def insert_money(self, amount: int) -> None:
        self._state.insert_money(amount)

    def select_product(self, product: str) -> None:
        self._state.select_product(product)

    def dispense_product(self) -> None:
        self._state.dispense_product()

    def refund(self) -> None:
        self._state.refund()

    def add_money(self, amount: int) -> None:
        self._current_money += amount

    def get_current_money(self) -> int:
        return self._current_money

    def reset_money(self) -> None:
        self._current_money = 0

    def get_product_price(self, product: str) -> Optional[int]:
        if product in self._inventory:
            return self._inventory[product]["price"]
        return None

    def get_product_name(self, product: str) -> Optional[str]:
        if product in self._inventory:
            return self._inventory[product]["name"]
        return None

    def dispense(self, product: str) -> None:
        if product in self._inventory and self._inventory[product]["quantity"] > 0:
            self._inventory[product]["quantity"] -= 1
            print(f"Dispensing {self._inventory[product]['name']}")
        
        # Check if machine is now sold out
        if all(item["quantity"] == 0 for item in self._inventory.values()):
            self.set_state(self._sold_out_state)

    def show_inventory(self) -> None:
        print("\nCurrent Inventory:")
        print("-" * 40)
        for code, item in self._inventory.items():
            print(f"{code}: {item['name']} - ${item['price']} "
                  f"(Quantity: {item['quantity']})")


class NoMoneyState(VendingMachineState):
    """Concrete State: No money inserted"""
    def __init__(self, machine: VendingMachine):
        self._machine = machine

    def insert_money(self, amount: int) -> None:
        self._machine.add_money(amount)
        print(f"${amount} inserted. Current balance: ${self._machine.get_current_money()}")
        self._machine.set_state(self._machine.get_has_money_state())

    def select_product(self, product: str) -> None:
        print("Please insert money first")

    def dispense_product(self) -> None:
        print("Please insert money first")

    def refund(self) -> None:
        print("No money to refund")


class HasMoneyState(VendingMachineState):
    """Concrete State: Has money, waiting for selection"""
    def __init__(self, machine: VendingMachine):
        self._machine = machine

    def insert_money(self, amount: int) -> None:
        self._machine.add_money(amount)
        print(f"${amount} inserted. Current balance: ${self._machine.get_current_money()}")

    def select_product(self, product: str) -> None:
        price = self._machine.get_product_price(product)
        if not price:
            print("Invalid product selection")
            return

        if self._machine.get_current_money() >= price:
            print(f"Selected {self._machine.get_product_name(product)}")
            self._machine._selected_product = product
            self._machine.set_state(self._machine.get_sold_state())
            self._machine.dispense_product()
        else:
            print(f"Insufficient funds. Need ${price - self._machine.get_current_money()} more")

    def dispense_product(self) -> None:
        print("Please select a product first")

    def refund(self) -> None:
        amount = self._machine.get_current_money()
        if amount > 0:
            print(f"Refunding ${amount}")
            self._machine.reset_money()
            self._machine.set_state(self._machine.get_no_money_state())


class SoldState(VendingMachineState):
    """Concrete State: Product selected, dispensing"""
    def __init__(self, machine: VendingMachine):
        self._machine = machine

    def insert_money(self, amount: int) -> None:
        print("Please wait, dispensing product")

    def select_product(self, product: str) -> None:
        print("Please wait, dispensing product")

    def dispense_product(self) -> None:
        if self._machine._selected_product:
            product = self._machine._selected_product
            price = self._machine.get_product_price(product)
            self._machine.dispense(product)
            self._machine.reset_money()
            self._machine._selected_product = None
            print(f"Thank you for your purchase! (${price})")
            self._machine.set_state(self._machine.get_no_money_state())

    def refund(self) -> None:
        print("Cannot refund after product is selected")


class SoldOutState(VendingMachineState):
    """Concrete State: All products sold out"""
    def __init__(self, machine: VendingMachine):
        self._machine = machine

    def insert_money(self, amount: int) -> None:
        print("Machine is sold out, cannot accept money")

    def select_product(self, product: str) -> None:
        print("Machine is sold out")

    def dispense_product(self) -> None:
        print("Machine is sold out")

    def refund(self) -> None:
        amount = self._machine.get_current_money()
        if amount > 0:
            print(f"Refunding ${amount}")
            self._machine.reset_money()


def main():
    # Create vending machine
    machine = VendingMachine()

    # Show initial inventory
    machine.show_inventory()

    # Test various operations
    print("\nTesting vending machine operations:")
    print("-" * 40)

    # Try to select without money
    machine.select_product("A1")

    # Insert money and select product
    machine.insert_money(1)
    machine.insert_money(1)
    machine.select_product("A1")  # Cola costs $2

    # Insert insufficient money
    machine.insert_money(1)
    machine.select_product("A1")

    # Request refund
    machine.refund()

    # Buy multiple items until sold out
    print("\nBuying all Cola...")
    for _ in range(5):
        machine.insert_money(2)
        machine.select_product("A1")

    # Try to buy sold out product
    machine.insert_money(2)
    machine.select_product("A1")

    # Show final inventory
    machine.show_inventory()


if __name__ == "__main__":
    main()
