import yaml, pytest

def test_template_yaml_valid():
    with open("template.yaml", "r") as f:
        data = yaml.safe_load(f)
        assert "signals" in data
        assert isinstance(data["signals"], list)
