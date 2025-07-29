def test_novice_persona_entry_logic():
    import yaml
    t = yaml.safe_load(open("template.yaml"))
    p = yaml.safe_load(open("persona_presets.yaml"))["novice_plus"]
    assert p["entry_radar"] == "active"
    assert any(s["trigger"] == "on-entry-price" for s in t["signals"])
