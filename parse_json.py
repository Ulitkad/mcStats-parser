import json

def get_nested_value(data, keys):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return 0
    return current

def get_data(input_dir, file_name, parameters):

    with open(f"{input_dir}/{file_name}", "r", encoding="utf-8") as file:
        data = json.load(file)

    result = get_nested_value(data, parameters)

    return result, input_dir


