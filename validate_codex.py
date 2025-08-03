"""Simple Codex Configuration Validator"""

import json
import sys
import yaml
from jsonschema import validate, ValidationError


def main():
    """Validate config.yaml against schema."""
    try:
        # Load config
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Load schema
        with open("schema/codex_validator_schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)

        # Validate against JSON schema
        validate(instance=config, schema=schema)

        print("SUCCESS: Config validation passed!")
        return True

    except FileNotFoundError as e:
        print(f"ERROR: File not found - {e}")
        return False

    except yaml.YAMLError as e:
        print(f"ERROR: YAML parsing failed - {e}")
        return False

    except json.JSONDecodeError as e:
        print(f"ERROR: JSON parsing failed - {e}")
        return False

    except ValidationError as e:
        print(f"ERROR: Schema validation failed - {e.message}")
        return False

    except Exception as e:
        print(f"ERROR: Unexpected error - {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
