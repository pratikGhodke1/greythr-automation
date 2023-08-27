"""Service Helpers"""

import random
from datetime import datetime, timedelta, time


def identify_current_schedule_cycle_start() -> datetime:
    """Get current schedule cycle start time."""
    now = datetime.now()

    if now.hour == 9:
        return datetime.combine(datetime.now(), time(9, 0))
    else:
        return datetime.combine(datetime.now(), time(19, 30))


def get_optimal_end_duration(total_employees: int):
    """Get a optimal end time to finish all signing activity."""
    if total_employees < 3:
        return 3
    elif total_employees < 10:
        return 30
    else:
        return 60


def get_random_datetime(start_time: datetime, total_employees: int) -> datetime:
    """Get randomg datetime"""
    random_minutes = random.randint(0, get_optimal_end_duration(total_employees))
    random_timedelta = timedelta(minutes=random_minutes)
    return start_time + random_timedelta


def get_sign_action_schedule(total_employees: int) -> list:
    """Get sign action schedule for employees with sleep duration."""
    start_time = identify_current_schedule_cycle_start()
    random_datetimes = []

    for _ in range(total_employees):
        random_datetime = get_random_datetime(start_time, total_employees)

        if random_datetime in random_datetimes:
            while True:
                random_datetime = get_random_datetime(start_time, total_employees)
                if random_datetime not in random_datetimes:
                    break

        random_datetimes.append(random_datetime)

    random_datetimes = sorted(random_datetimes)
    dates = zip(
        [start_time] + random_datetimes,
        random_datetimes,
    )

    return [(dt2 - dt1).total_seconds() // 60 for dt1, dt2 in dates]
