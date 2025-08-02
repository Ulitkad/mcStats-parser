import argparse
import parse_json
from os import listdir
import os
from os.path import isfile, join
import json

parser = argparse.ArgumentParser(description="Обработка JSON-файла со статистикой")

parser.add_argument('--stats', required=True, help='Path to stats folder')
parser.add_argument('--usercache', required=True, help='Path to usercache.json')
parser.add_argument('--pars', required=True, help='Statistic path')

args = parser.parse_args()

path_to_stats = args.stats
path_to_usercache = args.usercache
parameters = args.pars.split(',')

total_count = 0

files = [f for f in listdir(path_to_stats) if isfile(join(path_to_stats, f))]

with open(path_to_usercache, encoding="utf-8") as f:
    usercache = json.load(f)

uuid_to_name = {entry["uuid"].lower(): entry["name"] for entry in usercache}

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
        parts.append(f"{days}d, ")
    if hours > 0:
        parts.append(f"{hours}h, ")
    if minutes > 0:
        parts.append(f"{minutes}m, ")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return ''.join(parts)

def parse_folder(files):
    results = []
    global total_count

    is_time = parameters[-1].endswith('_time')
    is_cm = parameters[-1].endswith('_cm')

    for file in files:
        value, _ = parse_json.get_data(path_to_stats, file, parameters)
        original_value = value


        if is_cm:
            result_value = round(value / 100000, 1)
        elif is_time:
            result_value = ticks_to_string(value)
        else:
            result_value = value

        uuid = file[:-5]
        name = uuid_to_name.get(uuid.lower(), uuid)

        data = {
            "name": name,
            "result": result_value,
            "raw_value": original_value
        }

        results.append(data)
        total_count += value

    results.sort(key=lambda x: x["raw_value"], reverse=True)

    for i, item in enumerate(results, start=1):
        item["position"] = i
        del item["raw_value"]

    return results

def create_file_name():
    parts = [p.split(":")[-1] for p in parameters[1:]]
    result_string = "_".join(parts)
    return result_string

results = parse_folder(files)

os.makedirs(f"results/{create_file_name()}", exist_ok=True)

if parameters[-1].endswith('_time'):
    total = {
        "total": ticks_to_string(total_count)
    }
elif parameters[-1].endswith('_cm'):
    total = {
        "total": round(total_count / 100000, 1)
    }
else:
    total = {
        "total": total_count
    }

with open(f"results/{create_file_name()}/rating.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

with open(f"results/{create_file_name()}/total.json", "w", encoding="utf-8") as file:
    json.dump(total, file, indent=4, ensure_ascii=False)
