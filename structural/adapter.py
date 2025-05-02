"""
Adapter Design Pattern

This pattern allows incompatible interfaces to work together by wrapping an object
in an adapter to make it compatible with another class. Example demonstrates
converting data from different sources into a standardized format.
"""
from abc import ABC, abstractmethod
from typing import Dict, List


class DataAnalyzer:
    """Target Interface"""
    def process_data(self, data: List[Dict[str, str]]) -> None:
        print("\nProcessing standardized data:")
        for record in data:
            print(f"Analyzing record: {record}")


class XMLData:
    """Incompatible interface (XML format)"""
    def __init__(self, records: List[str]):
        self.records = records

    def get_xml_data(self) -> List[str]:
        return self.records


class JSONData:
    """Incompatible interface (JSON format)"""
    def __init__(self, records: List[Dict]):
        self.records = records

    def get_json_data(self) -> List[Dict]:
        return self.records


class DataAdapter(ABC):
    """Abstract Adapter Interface"""
    @abstractmethod
    def convert_data(self) -> List[Dict[str, str]]:
        pass


class XMLDataAdapter(DataAdapter):
    """Concrete Adapter for XML data"""
    def __init__(self, xml_data: XMLData):
        self.xml_data = xml_data

    def convert_data(self) -> List[Dict[str, str]]:
        print("Converting XML data to standardized format...")
        standardized_data = []
        for record in self.xml_data.get_xml_data():
            # Simulate XML parsing
            name, value = record.replace('<record>', '').replace('</record>', '').split(':')
            standardized_data.append({"name": name.strip(), "value": value.strip()})
        return standardized_data


class JSONDataAdapter(DataAdapter):
    """Concrete Adapter for JSON data"""
    def __init__(self, json_data: JSONData):
        self.json_data = json_data

    def convert_data(self) -> List[Dict[str, str]]:
        print("Converting JSON data to standardized format...")
        standardized_data = []
        for record in self.json_data.get_json_data():
            standardized_data.append({
                "name": str(record.get("name", "")),
                "value": str(record.get("value", ""))
            })
        return standardized_data


def main():
    # Create a data analyzer
    analyzer = DataAnalyzer()

    # Sample XML data
    xml_data = XMLData([
        "<record>temperature: 25°C</record>",
        "<record>humidity: 60%</record>"
    ])
    
    # Sample JSON data
    json_data = JSONData([
        {"name": "pressure", "value": "1013hPa"},
        {"name": "wind_speed", "value": "15km/h"}
    ])

    # Process XML data using adapter
    xml_adapter = XMLDataAdapter(xml_data)
    analyzer.process_data(xml_adapter.convert_data())

    # Process JSON data using adapter
    json_adapter = JSONDataAdapter(json_data)
    analyzer.process_data(json_adapter.convert_data())


if __name__ == "__main__":
    main()
