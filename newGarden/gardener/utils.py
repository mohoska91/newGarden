from datetime import datetime, time
from re import compile


def get_now():
    return datetime.now()


def is_time_in_range(start: time, now: time, end: time) -> bool:
    return (
            start <
            now <
            end
    )


def minute_to_sec(minute):
    return minute * 60


def hour_to_minute(hour):
    return hour * 60


def day_to_hour(day):
    return day * 24


def day_to_sec(day):
    return minute_to_sec(hour_to_minute(day_to_hour(day)))


def hour_to_sec(hour):
    return minute_to_sec(hour_to_minute(hour))


UNIT_MAP = {
    "s": lambda value: value,
    "m": minute_to_sec,
    "h": hour_to_sec,
    "d": day_to_sec,
}