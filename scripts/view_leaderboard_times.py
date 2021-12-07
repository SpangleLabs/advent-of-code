import datetime
import json
from typing import List, Optional
from functools import cached_property

import requests

CONFIG_FILE = "leaderboard_config.json"
CACHE_FILE = "leaderboard_cache.json"


def fetch_leaderboard_data(leaderboard_id: int, session_cookie: str, year: int = None) -> dict:
    year = year or datetime.date.today().year
    api_url = f"https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_id}.json"
    resp = requests.get(api_url, cookies={"session": session_cookie})
    return resp.json()


def format_duration(dur: datetime.timedelta) -> str:
    seconds = dur.total_seconds()
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    if hours >= 100:
        days = seconds // 86400
        hours = hours % 24
        return f"{days:.0f}d{hours:.0f}h{minutes:.0f}m"
    if hours == 0:
        return f"{minutes:.0f}m{seconds % 60:.0f}s"
    return f"{hours:.0f}h{minutes:.0f}m"


def calc_col_widths(table: List[List[str]]) -> List[int]:
    return [
        max(len(row[col_num]) for row in table if len(row) > col_num)
        for col_num in range(len(table[0]))
    ]


class Leaderboard:
    def __init__(self, owner_id: str, year: int, members: List["LeaderboardMember"]):
        self.owner_id = owner_id
        self.year = year
        self.members = members

    @cached_property
    def owner_name(self) -> str:
        for member in self.members:
            if member.member_id == self.owner_id:
                return member.name
        return "Unknown"

    @cached_property
    def latest_day(self) -> int:
        return max(
            max(d.day for d in member.days)
            for member in self.members
        )

    @cached_property
    def sorted_members(self) -> List["LeaderboardMember"]:
        return sorted(self.members, key=lambda member: member.local_score, reverse=True)

    def render(self, *, show_times: bool = False, show_durations: bool = False, show_diff: bool = False) -> str:
        lines = [
            "-" * 80,
            f"Leaderboard: {self.owner_name}",
            f"Year: {self.year}"
        ]
        view_members = [member for member in self.sorted_members if member.days]
        if not view_members:
            return "\n".join(lines)
        member_tables = {
            member.member_id: member.render_table(
                show_times=show_times,
                show_durations=show_durations,
                show_diff=show_diff
            ) for member in view_members
        }
        day_tables = []
        for member_table in member_tables.values():
            day_tables.extend(member_table)
        col_widths = calc_col_widths(day_tables)
        for member in view_members:
            lines.append("-" * 10)
            lines.append(member.header())
            table = member_tables[member.member_id]
            for row in table:
                lines.append(
                    "  ".join(s.rjust(col_widths[col_num]) for col_num, s in enumerate(row))
                )
        return "\n".join(lines)

    @classmethod
    def from_data(cls, data: dict) -> "Leaderboard":
        year = int(data["event"])
        return cls(
            data["owner_id"],
            year,
            [LeaderboardMember.from_data(member, year) for member in data["members"].values()]
        )

    @classmethod
    def load_from_api(cls, leaderboard_id: int, session_cookie: str, year: int = None) -> "Leaderboard":
        data = fetch_leaderboard_data(leaderboard_id, session_cookie, year)
        return cls.from_data(data)

    @classmethod
    def load_from_api_or_cache(cls, leaderboard_id: int, session_cookie: str, year: int = None) -> "Leaderboard":
        year = year or datetime.date.today().year
        cache_data = {}
        try:
            with open(CACHE_FILE, "r") as f:
                cache_data = json.load(f)
        except FileNotFoundError:
            pass
        year_entry = cache_data.get(year, {})
        leaderboard_entry = year_entry.get(leaderboard_id, {})
        cache_ts = leaderboard_entry.get("cache_time")
        cache_time = None
        if cache_ts:
            cache_time = datetime.datetime.fromisoformat(cache_ts)
        if cache_time is None or (datetime.datetime.now() - cache_time).total_seconds() > 15*60:
            data = fetch_leaderboard_data(leaderboard_id, session_cookie, year)
            if year not in cache_data:
                cache_data[year] = {}
            cache_data[year][leaderboard_id] = {
                "cache_time": datetime.datetime.now().isoformat(),
                "data": data
            }
            with open(CACHE_FILE, "w") as f:
                json.dump(cache_data, f)
        return cls.from_data(cache_data[year][leaderboard_id]["data"])


class LeaderboardMember:
    def __init__(self, member_id: str, name: str, local_score: int, days: List["LeaderboardDay"], year: int):
        self.member_id = member_id
        self.name = name
        self.local_score = local_score
        self.days = days
        self.year = year

    @cached_property
    def stars(self) -> int:
        return len(self.days) + len([day for day in self.days if day.part_two is not None])

    @cached_property
    def sorted_days(self) -> List["LeaderboardDay"]:
        return sorted(self.days, key=lambda day: day.day)

    def day(self, day: int) -> Optional["LeaderboardDay"]:
        return next(filter(lambda d: d.day == day, self.days), None)

    @cached_property
    def latest_day(self) -> Optional[int]:
        if not self.days:
            return None
        return max(d.day for d in self.days)

    def render_table(
            self,
            *,
            show_times: bool = False,
            show_durations: bool = False,
            show_diff: bool = False
    ) -> List[List[str]]:
        table = []
        line = ["Day:"]
        if self.days:
            line.extend([f"Day {d}" for d in range(1, self.latest_day + 1)])
        table.append(line)
        if show_times:
            line = ["Time:"]
            if self.days:
                line.extend([
                    self.day(d).render_times() if self.day(d) else ""
                    for d in range(1, self.latest_day + 1)
                ])
            table.append(line)
        if show_durations:
            line = ["Duration:"]
            if self.days:
                line.extend([
                    self.day(d).render_durations() if self.day(d) else ""
                    for d in range(1, self.latest_day + 1)
                ])
            table.append(line)
        if show_diff:
            line = ["Diff:"]
            if self.days:
                line.extend([
                    self.day(d).diff() if self.day(d) else ""
                    for d in range(1, self.latest_day + 1)
                ])
            table.append(line)
        return table

    def header(self) -> str:
        name = self.name
        if not name:
            name = f"Anonymous user (#{self.member_id})"
        lines = [
            f"Name: {name}",
            f"Stars: {self.stars}",
            f"Score: {self.local_score}",
        ]
        return "\n".join(lines)

    def render(self, *, show_times: bool = False, show_durations: bool = False, show_diff: bool = False) -> str:
        lines = [self.header()]
        table = self.render_table(show_times=show_times, show_durations=show_durations, show_diff=show_diff)
        if table and self.days:
            col_widths = calc_col_widths(table)
            for row in table:
                lines.append(
                    "  ".join(s.rjust(col_widths[col_num]) for col_num, s in enumerate(row))
                )
        return "\n".join(lines)

    @classmethod
    def from_data(cls, data: dict, year: int) -> "LeaderboardMember":
        member_id = data["id"]
        name = data["name"]
        score = data["local_score"]
        days = [LeaderboardDay.from_data(int(day), value, year) for day, value in data["completion_day_level"].items()]
        return cls(member_id, name, score, days, year)


class LeaderboardDay:
    def __init__(
            self,
            day: int,
            part_one: "LeaderboardDayPart",
            part_two: Optional["LeaderboardDayPart"],
            year: int
    ) -> None:
        self.day = day
        self.part_one = part_one
        self.part_two = part_two
        self.year = year

    @cached_property
    def date(self) -> datetime.date:
        return datetime.date(self.year, 12, self.day)

    @cached_property
    def release_time(self) -> datetime.datetime:
        return datetime.datetime(self.year, 12, self.day, 5, 0, 0)

    def render_times(self) -> str:
        out = self.part_one.time_str()
        if self.part_two:
            out += f", {self.part_two.time_str(self.part_one.completion_datetime.date())}"
        else:
            out += ", --"
        return out

    def render_durations(self) -> str:
        out = self.part_one.duration_str()
        if self.part_two:
            out += f" +{self.diff()}"
        else:
            out += " +??"
        return out

    def diff(self) -> str:
        if self.part_two is None:
            return "1 star"
        return format_duration(self.part_two.completion_datetime - self.part_one.completion_datetime)

    @classmethod
    def from_data(cls, day: int, data: dict, year: int) -> "LeaderboardDay":
        one_ts = datetime.datetime.utcfromtimestamp(data["1"]["get_star_ts"])
        part_two = None
        if "2" in data:
            two_ts = datetime.datetime.utcfromtimestamp(data["2"]["get_star_ts"])
            part_two = LeaderboardDayPart(two_ts, day, year)
        return cls(
            day,
            LeaderboardDayPart(one_ts, day, year),
            part_two,
            year
        )


class LeaderboardDayPart:
    def __init__(self, completion_datetime: datetime.datetime, day: int, year: int) -> None:
        self.completion_datetime = completion_datetime
        self.day = day
        self.year = year

    @cached_property
    def date(self) -> datetime.date:
        return datetime.date(self.year, 12, self.day)

    @cached_property
    def release_time(self) -> datetime.datetime:
        return datetime.datetime(self.year, 12, self.day, 5, 0, 0)

    def time_str(self, compare_date: Optional[datetime.date] = None) -> str:
        compare_date = compare_date or self.date
        complete_date = self.completion_datetime.date()
        if complete_date == compare_date:
            return self.completion_datetime.strftime("%H:%M")
        if complete_date.month == compare_date.month and complete_date.year == compare_date.year:
            return self.completion_datetime.strftime("%dT%H:%M")
        return self.completion_datetime.strftime("%Y-%m-%dT%H:%M")

    def duration_str(self) -> str:
        return format_duration(self.completion_datetime - self.release_time)


if __name__ == "__main__":
    input_year = 2021
    with open(CONFIG_FILE, "r") as conf_file:
        conf = json.load(conf_file)
    for lid in conf["leaderboards"]:
        leaderboard = Leaderboard.load_from_api_or_cache(lid, conf["session_cookie"], input_year)
        print(leaderboard.render(
            show_times=True,
            show_durations=True,
            show_diff=True
        ))
