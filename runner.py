from glob import glob
from enum import Enum
from typing import Optional
import datetime
import importlib

from utils.types import is_int

scripts = ["create_new_day", "view_leaderboard_times"]
years = sorted([y[2:-1] for y in glob("./[0-9][0-9][0-9][0-9]/")])


class CoreChoice(Enum):
    DAILY = "0"
    SCRIPT = "1"


def choose_daily_or_script() -> Optional[CoreChoice]:
    resp = input("Would you like to run a daily solution [0] or a script [1]: ")
    if resp not in ["0", "1"]:
        print("Unrecognised input")
        return None
    return CoreChoice(resp)


def choose_date() -> Optional[datetime.date]:
    year = input(f"Which year would you like to run: ({', '.join(years)}) ")
    if year not in years:
        print("Year not recognised")
        return None
    days = sorted([d[7:-3] for d in glob(f"./{year}/[0-9][0-9].py")])
    day = input(f"Which day would you like to run: ({', '.join(days)}) ")
    if day not in days:
        print("Day not recognised")
        return None
    print(f"Year {year}, Day {day}")
    return datetime.date(int(year), 12, int(day))


def choose_script() -> Optional[str]:
    script_options = "\n".join(f"[{i}] {script}" for i, script in enumerate(scripts))
    resp = input(f"Which script would you like to run:\n{script_options}\nEnter number: ")
    if not is_int(resp) or not (0 <= int(resp) < len(scripts)):
        print("Unrecognised option.")
        return None
    return scripts[int(resp)]


def run_script(script: str) -> None:
    s = importlib.import_module(f"scripts.{script}")
    s._main()


def run_advent_date(date: datetime.date) -> None:
    i1 = importlib.import_module(f"{date.year}.{date.day}")
    start_time = datetime.datetime.now()
    print(i1._main())
    print(f"Part one took: {(datetime.datetime.now()-start_time).total_seconds()}s")
    i2 = importlib.import_module(f"{date.year}.{date.day}-2")
    start_time = datetime.datetime.now()
    print(i2._main())
    print(f"Part two took: {(datetime.datetime.now()-start_time).total_seconds()}s")


if __name__ == "__main__":
    core_choice = None
    while core_choice is None:
        core_choice = choose_daily_or_script()
    if core_choice == CoreChoice.DAILY:
        advent_date = None
        while advent_date is None:
            advent_date = choose_date()
        run_advent_date(advent_date)
        print(f"Running {advent_date}")  # TODO: run part 1 and 2, against test and input?
    elif core_choice == CoreChoice.SCRIPT:
        script_choice = None
        while script_choice is None:
            script_choice = choose_script()
        print(f"Script chosen: {script_choice}")  # TODO: run script
        run_script(script_choice)
    else:
        print("Unrecognised option.")
