import yaml, pytest

def test_template_yaml_valid():
    """Confirm the template.yaml file is properly formatted."""
    with open("template.yaml", "r") as file:
        try:
            data = yaml.safe_load(file)
            assert "signals" in data, "signals key is required"
            assert isinstance(data["signals"], list), "signal must be a list"
            required_keys = ["what_happened", "why_it_matters", "suggested_posture"]

            for signal in data["signals"]:
                for key in required_keys:
                    assert key in signal, f"{key} is required in each signal"
        except FileNotFoundError:
            pytest.fail("template.yaml not found")
        except yaml.YAMLError as e:
            pytest.fail(f"Error parsing YAML: {e}")
