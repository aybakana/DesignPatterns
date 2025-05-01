"""
Singleton Design Pattern

This pattern ensures a class has only one instance and provides a global point
of access to it. Example demonstrates a Configuration Manager.
"""

class ConfigurationManager:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_config(self, key: str, value: str) -> None:
        """Set a configuration value"""
        self._config[key] = value

    def get_config(self, key: str) -> str:
        """Get a configuration value"""
        return self._config.get(key)


# Example usage
def main():
    # Create first instance
    config1 = ConfigurationManager()
    config1.set_config("database_url", "postgresql://localhost:5432/db")

    # Create second instance - will be the same object
    config2 = ConfigurationManager()
    print(config2.get_config("database_url"))  # Output: postgresql://localhost:5432/db
    
    # Prove both are the same instance
    print(f"Are config1 and config2 the same instance? {config1 is config2}")  # True

if __name__ == "__main__":
    main()
