from datetime import date, datetime
from zoneinfo import ZoneInfo

APP_TIMEZONE = ZoneInfo("Europe/Moscow")

def today() -> date:
    return datetime.now(APP_TIMEZONE).date()

def trip_status(start_date: date, end_date: date, current: date) -> str:
    if current < start_date:
        return "upcoming"
    if current > end_date:
        return "finished"
    return "ongoing"

def days_until(start_date: date, current: date) -> int | None:
    if current >= start_date:
        return None
    return (start_date - current).days