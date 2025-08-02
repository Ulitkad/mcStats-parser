import argparse
import parse_json
from os import listdir
import os
from os.path import isfile, join
import json

parser = argparse.ArgumentParser(description="Create leaderboard from player statistics")

parser.add_argument('--stats', required=True, help='Path to stats folder')
parser.add_argument('--usercache', required=True, help='Path to usercache.json')
parser.add_argument('--params', required=True, help='Comma-separated statistic paths, e.g., "minecraft:custom,minecraft:broken,minecraft:shield"')
parser.add_argument('--exclude-zero', action='store_true', help='Exclude players with zero value from the leaderboard')

args = parser.parse_args()

path_to_stats = args.stats
path_to_usercache = args.usercache
parameters = args.params.split(',')

files = [f for f in listdir(path_to_stats) if isfile(join(path_to_stats, f))]

try:
    with open(path_to_usercache, encoding="utf-8") as f:
        usercache = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error while reading usercache.json: {e}")
    exit(1)

uuid_to_name = {entry["uuid"].lower(): entry["name"] for entry in usercache}


def format_value(value, parameters):
    if "_cm" in parameters[-1]:
        result_value = cm_to_kilometers(value)
    elif "time" in parameters[-1]:
        result_value = ticks_to_string(value)
    else:
        result_value = value
    return result_value


def ticks_to_string(ticks):
    seconds = ticks // 20
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return ', '.join(parts)


def cm_to_kilometers(cm):
    kilometrs = round(cm / 100000)
    return f'{kilometrs}km'


def parse_folder(files, exclude_zero=False):
    results = []
    total_count = 0

    for file in files:
        value = parse_json.get_data(path_to_stats, file, parameters)

        if exclude_zero and value == 0:
            continue

        uuid = file[:-5]
        name = uuid_to_name.get(uuid.lower(), uuid)
        result_value = format_value(value, parameters)

        data = {
            "name": name,
            "result": result_value,
            "raw_value": value
        }

        results.append(data)

    results.sort(key=lambda x: x["raw_value"], reverse=True)

    for i, item in enumerate(results, start=1):
        item["position"] = i
        total_count += item["raw_value"]
        del item["raw_value"]

    total_count = format_value(total_count, parameters)

    return results, total_count


def create_file_name():
    parts = [p.split(":")[-1] for p in parameters[1:]]
    result_string = "_".join(parts)
    return result_string


def write_results():
    results,total_count = parse_folder(files, exclude_zero=args.exclude_zero)
    folder_name = create_file_name()
    folder_path = os.path.join("results", folder_name)

    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, "rating.json"), "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    with open(os.path.join(folder_path, "total.json"), "w", encoding="utf-8") as file:
        json.dump(total_count, file, indent=4, ensure_ascii=False)

    print(f"Successfully created leaderboard in {folder_path}")


write_results()