"""Tests for validate_codex.py"""
import pytest
import yaml
import json
from validate_codex import main

def test_config_validation_passes():
    """Test that valid config passes validation"""
    result = main()
    assert result is True

def test_schema_exists():
    """Test that schema file exists and is valid JSON"""
    with open('schema/codex_validator_schema.json', 'r') as f:
        schema = json.load(f)
    assert 'properties' in schema
    assert 'required' in schema