"""
Observer Design Pattern

This pattern defines a one-to-many dependency between objects so that when one
object changes state, all its dependents are notified and updated automatically.
Example demonstrates a weather monitoring system with multiple display types.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Observer(ABC):
    """Abstract Observer"""
    @abstractmethod
    def update(self, data: Dict[str, Any]) -> None:
        pass


class Subject(ABC):
    """Abstract Subject"""
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class WeatherStation(Subject):
    """Concrete Subject"""
    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Attached {observer.__class__.__name__}")

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Detached {observer.__class__.__name__}")

    def notify(self) -> None:
        data = {
            'temperature': self._temperature,
            'humidity': self._humidity,
            'pressure': self._pressure
        }
        for observer in self._observers:
            observer.update(data)

    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        print("\nWeather station updating measurements...")
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify()


class CurrentConditionsDisplay(Observer):
    """Concrete Observer displaying current conditions"""
    def update(self, data: Dict[str, Any]) -> None:
        print("\nCurrent Conditions:")
        print(f"Temperature: {data['temperature']}°C")
        print(f"Humidity: {data['humidity']}%")
        print(f"Pressure: {data['pressure']} hPa")


class StatisticsDisplay(Observer):
    """Concrete Observer displaying statistics"""
    def __init__(self):
        self._temperature_readings: List[float] = []
        self._humidity_readings: List[float] = []
        self._pressure_readings: List[float] = []

    def update(self, data: Dict[str, Any]) -> None:
        self._temperature_readings.append(data['temperature'])
        self._humidity_readings.append(data['humidity'])
        self._pressure_readings.append(data['pressure'])

        print("\nWeather Statistics:")
        print(f"Average temperature: {sum(self._temperature_readings) / len(self._temperature_readings):.1f}°C")
        print(f"Average humidity: {sum(self._humidity_readings) / len(self._humidity_readings):.1f}%")
        print(f"Average pressure: {sum(self._pressure_readings) / len(self._pressure_readings):.1f} hPa")


class ForecastDisplay(Observer):
    """Concrete Observer displaying weather forecast"""
    def __init__(self):
        self._last_pressure = 0.0

    def update(self, data: Dict[str, Any]) -> None:
        current_pressure = data['pressure']
        print("\nWeather Forecast:")
        if current_pressure > self._last_pressure:
            print("Improving weather on the way!")
        elif current_pressure < self._last_pressure:
            print("Watch out for cooler, rainy weather")
        else:
            print("More of the same")
        self._last_pressure = current_pressure


def main():
    # Create the WeatherStation
    weather_station = WeatherStation()

    # Create display elements
    current_display = CurrentConditionsDisplay()
    statistics_display = StatisticsDisplay()
    forecast_display = ForecastDisplay()

    # Register observers
    weather_station.attach(current_display)
    weather_station.attach(statistics_display)
    weather_station.attach(forecast_display)

    # Simulate weather changes
    print("\nSimulating weather changes:")
    print("-" * 50)
    
    # First weather update
    weather_station.set_measurements(24.5, 65.0, 1013.1)

    # Second weather update
    weather_station.set_measurements(23.8, 70.0, 1012.5)

    # Remove forecast display
    weather_station.detach(forecast_display)

    # Third weather update (without forecast)
    weather_station.set_measurements(25.1, 63.0, 1014.2)


if __name__ == "__main__":
    main()
