import os
import json

json_path = os.path.join(
    os.path.dirname(__file__),
    "data",
    "equipment_list.json"   # <-- UPDATED NAME
)

print("Looking for:", json_path)
print("Exists:", os.path.exists(json_path))

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    print("Loaded OK. Items:", len(data))
