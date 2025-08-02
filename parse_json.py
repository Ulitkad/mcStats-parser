import json
import os

def get_nested_value(data, keys):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return 0
    return current

def get_data(input_dir, file_name, parameters):

    try:
        with open(os.path.join(input_dir, file_name), "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error while reading {file_name}: {e}")
        return 0

    result = get_nested_value(data, parameters)

    return result


