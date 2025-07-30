import json
import yaml
import sys
import jsonschema
from jsonschema import validate, ValidationError, SchemaError

TEMPLATE_PATH = "template.yaml"
SCHEMA_PATH = "schema/codex_validator_schema.json"

with open("template.yaml", "r") as f:
    data = yaml.safe_load(f)

with open("schema/codex_validator_schema.json", "r") as f:
    schema = json.load(f)

jsonschema.validate(instance=data, schema=schema)
print("✅ Schema validation passed.")

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    try:
        data = load_yaml(TEMPLATE_PATH)
        schema = load_json(SCHEMA_PATH)
        validate(instance=data, schema=schema)
        print("✅ Codex schema validation passed.")
    except FileNotFoundError as e:
        print(f"❌ File not found: {e.filename}")
        sys.exit(1)
    except ValidationError as e:
        print(f"❌ Schema validation failed:\n  → {e.message}")
        sys.exit(1)
    except SchemaError as e:
        print(f"❌ Invalid schema:\n  → {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error:\n  → {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
