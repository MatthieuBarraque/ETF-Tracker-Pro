import json
from error_handler import ConfigError

def load_json(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: {filepath}")
    except json.JSONDecodeError:
        raise ConfigError(f"Error decoding JSON from file: {filepath}")
