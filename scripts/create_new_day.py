import json
import os
import re
import shutil
from datetime import datetime
from typing import Optional

import requests

from scripts.leaderboard import CONFIG_FILE

CODE_TEMPLATE = """
from utils.input import load_lines

if __name__ == "__main__":
    my_input = load_lines(test=True)
    print("Good luck!")
"""


def find_example(page_url, cookie: str) -> Optional[str]:
    example_pattern = re.compile(r"For example.*:</p>\n<pre><code>((?:.|\n)+?)</code>")
    tag_pattern = re.compile(r"<[a-z/]>")
    page_data = requests.get(page_url, cookies={"session": cookie}).content.decode()
    examples = []
    for match in example_pattern.finditer(page_data):
        raw_data = match.group(1)
        tag_pattern.sub("", raw_data)
        examples.append(raw_data)
    if examples:
        return examples[0]


def setup_day(year: int, day: int, cookie: str) -> None:
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    part_1_file = base_dir + f"/{year}/{day}.py"
    part_2_file = base_dir + f"/{year}/{day}-2.py"
    test_file = base_dir + f"/{year}/{day}-test.txt"
    input_file = base_dir + f"/{year}/{day}-input.txt"
    if os.path.exists(part_1_file):
        print("Files already exist for today")
        # Create part 2 file
        if not os.path.exists(part_2_file):
            print("But not part two, copying part 1..")
            shutil.copy(part_1_file, part_2_file)
        return
    page_url = f"https://adventofcode.com/{year}/day/{day}"
    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    # Create code file
    print("Creating code file from template")
    with open(part_1_file, "w") as f:
        f.write(CODE_TEMPLATE)
    # Get input data
    input_data = requests.get(input_url, cookies={"session": cookie}).content
    print("Saving input data")
    with open(input_file, "wb") as f:
        f.write(input_data)
    # Find test data
    example = find_example(page_url, cookie)
    if example:
        print("Example found, saving as test data")
        with open(test_file, "w") as f:
            f.write(example)


if __name__ == "__main__":
    y = 2021
    d = datetime.today().day
    with open(CONFIG_FILE, "r") as conf_file:
        conf = json.load(conf_file)
    setup_day(y, d, conf["session_cookie"])
