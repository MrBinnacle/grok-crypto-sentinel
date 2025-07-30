# tests/test_codex_schema.py

import json
import yaml
import jsonschema
from pathlib import Path

def test_template_yaml_is_valid():
    base = Path(__file__).resolve().parent.parent
    template_path = base / "template.yaml"
    schema_path = base / "schema" / "codex_validator_schema.json"

    with template_path.open() as y:
        data = yaml.safe_load(y)

    with schema_path.open() as s:
        schema = json.load(s)

    jsonschema.validate(instance=data, schema=schema)
