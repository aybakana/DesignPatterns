"""
Template Design Pattern

This pattern defines the skeleton of an algorithm in a method, deferring some steps
to subclasses. Example demonstrates a data mining framework for different file types.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import csv
from pathlib import Path


class DataMiner(ABC):
    """Abstract Template class"""
    def mine_data(self, path: str) -> None:
        """Template method defining the data mining algorithm"""
        # Common steps for all data miners
        file_content = self._read_file(path)
        raw_data = self._parse_data(file_content)
        structured_data = self._process_data(raw_data)
        self._analyze_data(structured_data)
        self._send_report()

        # Optional step - hook method
        if self._should_save_to_database():
            self._save_to_database(structured_data)

    @abstractmethod
    def _read_file(self, path: str) -> str:
        """Read the file content"""
        pass

    @abstractmethod
    def _parse_data(self, content: str) -> Any:
        """Parse the raw content into initial data structure"""
        pass

    def _process_data(self, data: Any) -> List[Dict[str, Any]]:
        """Process the parsed data into a standard format
        This is a concrete method as the processing is common for all miners"""
        print("Processing data into standard format...")
        # Convert data to list of dictionaries if not already
        if isinstance(data, list):
            return data
        return [{"data": data}]

    def _analyze_data(self, data: List[Dict[str, Any]]) -> None:
        """Analyze the processed data"""
        print("\nAnalyzing data:")
        print(f"Number of records: {len(data)}")
        print("Sample data:", data[:2])

    def _send_report(self) -> None:
        """Send analysis report"""
        print("Sending analysis report via email...")

    def _should_save_to_database(self) -> bool:
        """Hook method - can be overridden by subclasses"""
        return True

    def _save_to_database(self, data: List[Dict[str, Any]]) -> None:
        """Save the processed data to database"""
        print("Saving data to database...")


class JSONDataMiner(DataMiner):
    """Concrete class for mining JSON data"""
    def _read_file(self, path: str) -> str:
        print(f"\nReading JSON file: {path}")
        with open(path, 'r') as file:
            return file.read()

    def _parse_data(self, content: str) -> List[Dict[str, Any]]:
        print("Parsing JSON data...")
        return json.loads(content)


class CSVDataMiner(DataMiner):
    """Concrete class for mining CSV data"""
    def _read_file(self, path: str) -> str:
        print(f"\nReading CSV file: {path}")
        with open(path, 'r') as file:
            return file.read()

    def _parse_data(self, content: str) -> List[Dict[str, Any]]:
        print("Parsing CSV data...")
        results = []
        lines = content.strip().split('\n')
        if not lines:
            return results

        headers = lines[0].split(',')
        for line in lines[1:]:
            values = line.split(',')
            results.append(dict(zip(headers, values)))
        return results

    def _should_save_to_database(self) -> bool:
        """Override hook method"""
        return False  # Don't save CSV data to database


class LogDataMiner(DataMiner):
    """Concrete class for mining log files"""
    def _read_file(self, path: str) -> str:
        print(f"\nReading log file: {path}")
        with open(path, 'r') as file:
            return file.read()

    def _parse_data(self, content: str) -> List[Dict[str, Any]]:
        print("Parsing log data...")
        results = []
        for line in content.strip().split('\n'):
            if line:
                # Simple log format: timestamp - level - message
                parts = line.split(' - ', 2)
                if len(parts) == 3:
                    results.append({
                        'timestamp': parts[0],
                        'level': parts[1],
                        'message': parts[2]
                    })
        return results


def create_sample_files():
    """Create sample files for demonstration"""
    # Create sample JSON file
    json_data = [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Jane", "age": 25}
    ]
    with open('sample.json', 'w') as f:
        json.dump(json_data, f)

    # Create sample CSV file
    csv_data = [
        ['name', 'age', 'city'],
        ['John', '30', 'New York'],
        ['Jane', '25', 'San Francisco']
    ]
    with open('sample.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    # Create sample log file
    log_data = [
        "2023-05-01 10:00:00 - INFO - Application started",
        "2023-05-01 10:01:15 - WARNING - High memory usage",
        "2023-05-01 10:02:30 - ERROR - Database connection failed"
    ]
    with open('sample.log', 'w') as f:
        f.write('\n'.join(log_data))


def main():
    # Create sample files
    create_sample_files()

    # Process JSON data
    json_miner = JSONDataMiner()
    json_miner.mine_data('sample.json')

    # Process CSV data
    csv_miner = CSVDataMiner()
    csv_miner.mine_data('sample.csv')

    # Process log data
    log_miner = LogDataMiner()
    log_miner.mine_data('sample.log')

    # Clean up sample files
    for file in ['sample.json', 'sample.csv', 'sample.log']:
        Path(file).unlink()


if __name__ == "__main__":
    main()
