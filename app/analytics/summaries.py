from datetime import date


def format_period(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"
