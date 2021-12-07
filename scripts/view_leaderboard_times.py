import datetime
import json

import requests

if __name__ == "__main__":
    year = 2021
    with open("leaderboard_config.json", "r") as f:
        conf = json.load(f)
    for leaderboard in conf["leaderboards"]:
        api_url = f"https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard}.json"
        resp = requests.get(api_url, cookies={"session": conf["session_cookie"]})
        data = resp.json()
        with open(f"leaderboard_{leaderboard}.json", "w") as f:
            json.dump(data, f)
        owner_name = data["members"][data["owner_id"]]["name"]
        last_day = max(max([0, *(int(x) for x in member["completion_day_level"].keys())]) for member in data["members"].values())
        print(f"Leaderboard: {owner_name}")
        for member in data["members"].values():
            name = member["name"]
            score = member["local_score"]
            time_data = []
            dur_data = []
            for day in range(1, last_day + 1):
                release_time = datetime.datetime(year, 12, day, 5, 0, 0)
                if str(day) in member["completion_day_level"]:
                    completion_time_1 = datetime.datetime.utcfromtimestamp(member["completion_day_level"][str(day)]["1"]["get_star_ts"])
                    time_str = f"{completion_time_1.strftime('%H:%M ')} "
                    duration_1 = (completion_time_1 - release_time).total_seconds()
                    dur_str_1 = f"{duration_1 // 3600:02.0f}h{(duration_1 % 3600) // 60:02.0f}m"
                    dur_str_2 = "--h--m"
                    if "2" in member["completion_day_level"][str(day)]:
                        completion_time_2 = datetime.datetime.utcfromtimestamp(member["completion_day_level"][str(day)]["2"]["get_star_ts"])
                        time_str += f"{completion_time_2.strftime('%H:%M ')}"
                        duration_2 = (completion_time_2 - release_time).total_seconds()
                        dur_str_2 = f"{duration_2 // 3600:02.0f}h{(duration_2 % 3600) // 60:02.0f}m"
                    else:
                        time_str += "--:--"
                    time_data.append(time_str)
                    dur_data.append(f"{dur_str_1}-{dur_str_2}")
                else:
                    time_data.append("--:-- --:--")
                    dur_data.append("--h--m --h--m")
            print(f"{name}: {score}")
            print("  ".join(time_data))
            print("  ".join(dur_data))
