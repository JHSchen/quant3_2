import json
from jsonschema import validate, ValidationError

def validate_json(file_path, schema_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    try:
        validate(instance=data, schema=schema)
        print(f"✅ {file_path} is valid against {schema_path}")
    except ValidationError as e:
        print(f"❌ {file_path} validation failed: {e.message}")

if __name__ == "__main__":
    validate_json('portfolio/AVGO_protocol.json', 'docs/schemas/protocol.schema.json')
    validate_json('portfolio/active_portfolio_monitor.json', 'docs/schemas/monitor.schema.json')
