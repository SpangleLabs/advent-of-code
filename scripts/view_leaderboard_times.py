import json

from scripts.leaderboard import Leaderboard, CONFIG_FILE

if __name__ == "__main__":
    input_year = 2021
    for input_year in range(2015, 2022):
        with open(CONFIG_FILE, "r") as conf_file:
            conf = json.load(conf_file)
        for lid in conf["leaderboards"]:
            leaderboard = Leaderboard.load_from_api_or_cache(str(lid), conf["session_cookie"], input_year)
            print(leaderboard.render(
                show_times=True,
                show_durations=True,
                show_diff=True
            ))
