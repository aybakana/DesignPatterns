"""
Builder Design Pattern

This pattern separates the construction of a complex object from its representation,
allowing the same construction process to create different representations.
Example demonstrates a computer builder.
"""
from abc import ABC, abstractmethod
from typing import Any


class Computer:
    """Product"""
    def __init__(self):
        self.parts = {}

    def add_part(self, key: str, value: Any):
        self.parts[key] = value

    def show_specs(self):
        print("Computer Specifications:")
        for key, value in self.parts.items():
            print(f"{key}: {value}")


class ComputerBuilder(ABC):
    """Abstract Builder"""
    def __init__(self):
        self.computer = Computer()

    @abstractmethod
    def add_cpu(self):
        pass

    @abstractmethod
    def add_memory(self):
        pass

    @abstractmethod
    def add_storage(self):
        pass

    @abstractmethod
    def add_gpu(self):
        pass

    def get_computer(self) -> Computer:
        return self.computer


class GamingComputerBuilder(ComputerBuilder):
    """Concrete Builder for Gaming PC"""
    def add_cpu(self):
        self.computer.add_part("CPU", "AMD Ryzen 9 5950X")
        return self

    def add_memory(self):
        self.computer.add_part("Memory", "32GB DDR4 3600MHz")
        return self

    def add_storage(self):
        self.computer.add_part("Storage", "2TB NVMe SSD")
        return self

    def add_gpu(self):
        self.computer.add_part("GPU", "NVIDIA RTX 4090")
        return self


class OfficeComputerBuilder(ComputerBuilder):
    """Concrete Builder for Office PC"""
    def add_cpu(self):
        self.computer.add_part("CPU", "Intel i5-12400")
        return self

    def add_memory(self):
        self.computer.add_part("Memory", "16GB DDR4 3200MHz")
        return self

    def add_storage(self):
        self.computer.add_part("Storage", "512GB SATA SSD")
        return self

    def add_gpu(self):
        self.computer.add_part("GPU", "Intel UHD Graphics 730")
        return self


class Director:
    """Director"""
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder

    def construct_computer(self):
        return (self.builder
                .add_cpu()
                .add_memory()
                .add_storage()
                .add_gpu()
                .get_computer())


# Example usage
def main():
    # Build a gaming computer
    gaming_builder = GamingComputerBuilder()
    director = Director(gaming_builder)
    gaming_pc = director.construct_computer()
    print("Gaming PC:")
    gaming_pc.show_specs()

    print("\n")

    # Build an office computer
    office_builder = OfficeComputerBuilder()
    director = Director(office_builder)
    office_pc = director.construct_computer()
    print("Office PC:")
    office_pc.show_specs()


if __name__ == "__main__":
    main()
