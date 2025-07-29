def test_output_blocks():
    with open("examples/sample_output_sniper.md") as f:
        text = f.read()
    assert "📆" in text
    assert "🧠 Daily Reflection" in text
    assert "Entry Radar" in text
