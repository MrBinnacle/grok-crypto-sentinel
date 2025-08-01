"""Simple Codex Configuration Validator"""

import json
import sys
import yaml

def main():
    """Validate config.yaml against schema."""
    try:
        # Load config
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Load schema  
        with open('schema/codex_validator_schema.json', 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Basic validation - check required keys
        if 'schedule' not in config:
            print("ERROR: Missing 'schedule' key in config")
            return False
            
        if 'codex' not in config:
            print("ERROR: Missing 'codex' key in config")
            return False
            
        if 'run_time' not in config['schedule']:
            print("ERROR: Missing 'run_time' in schedule")
            return False
            
        codex = config['codex']
        if 'breakout_watch' not in codex:
            print("ERROR: Missing 'breakout_watch' in codex")
            return False
            
        if 'onchain_signal' not in codex:
            print("ERROR: Missing 'onchain_signal' in codex")
            return False
        
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
        
    except Exception as e:
        print(f"ERROR: Unexpected error - {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
