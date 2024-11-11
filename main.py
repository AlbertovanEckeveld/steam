import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            return json_data
    except FileNotFoundError:
        print("File not found.")
        return None

file_path = "steam.json"
json_data = read_json_file(file_path)

if json_data is not None:
    print(json.dumps(json_data, indent=4))
else:
    print("Failed to parse JSON data.")