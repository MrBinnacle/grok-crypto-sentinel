import yaml

def test_signal_structure():
    with open("template.yaml") as f:
        data = yaml.safe_load(f)
    for signal in data.get("signals", []):
        assert "trigger" in signal
        assert "conditions" in signal
        assert isinstance(signal["trigger"], str)
