# mcStats-parser

Python script to parse player statistics from Minecraft's `stats` folder and generate a leaderboard.

## How it works

- Reads `.json` stat files from the specified directory.
- Extracts a given statistic key (e.g., `minecraft:mined:minecraft:stone`).
- Detects the value type (time, distance, etc.) and formats it.
- Maps each player's UUID to their username using `usercache.json`.
- Sorts players by their stat values in descending order.
- Outputs two files:
  - `rating.json`: list of players with results and ranking.
  - `total.json`: total value across all players.

## Usage

Example usage:
```bash
# Path to stats dir and usercache.json through home
python main.py --stats ~/server/world/stats --usercache ~/server/usercache.json --params stats,minecraft:broken,minecraft:shield

# Path to stats dir and usercache.json in current directory
python main.py --stats stats --usercache usercache.json --params stats,minecraft:broken,minecraft:shield --exclude-zero
```

Command arguments:
| Parameter   | Description             | Example                          |
|-------------|-------------------------|---------------------------------|
| --stats     | Path to stats/ directory| ~/server/world/stats            |
| --usercache | Path to usercache.json  | ~/server/usercache.json         |
| --params      | Stats to collect        | stats,minecraft:broken,minecraft:shield |
| --exclude-zero | Exclude players with `"result": 0` | |


## How to determine what to use in --params

To specify the correct statistic path for the `--params` argument, follow these steps:

1. **Locate a player's stats file**  
    Go to the `stats/` folder inside your Minecraft world save (e.g. `world/stats/`). Open any `.json` file inside.

2. **Inspect the structure**  
    Open the JSON file and look for the `"stats"` object. Inside, statistics are grouped by categories like `"minecraft:custom"`, `"minecraft:broken"`, `"minecraft:used"`, etc.

3. **Choose a statistic path**  
    Navigate through the nested keys to find the statistic you're interested in.  
    Example:
    ```json
    {
      "stats": {
        "minecraft:custom": {
          "minecraft:jump": 523,
          "minecraft:walk_one_cm": 104293
        }
      }
    }
    ```
    If you want to track total jumps, the full path would be:
    stats,minecraft:custom,minecraft:jump

4. **Pass it to the script**
    Use that full path as the --params value:
    ```bash
    python script.py --stats path/to/stats --usercache path/to/usercache.json --params stats,minecraft:custom,minecraft:jump
    ```
