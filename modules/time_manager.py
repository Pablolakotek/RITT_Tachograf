from enum import Enum
from datetime import datetime

class TimeType(Enum):
    DRIVE = "drive_time"
    WORK = "work_time"
    BREAK = "break_time"

class TimeManager:
    def __init__(self):
        self.times = {TimeType.DRIVE: 0, TimeType.WORK: 0, TimeType.BREAK: 0}
        self.break_remaining_time = 0
        self.drive_time_violations = 0
        self.work_time_violations = 0

    def calculate_delta_time(self, current_time, last_time):
        """Oblicza różnicę czasu gry w sekundach."""
        delta_time = current_time - last_time
        if delta_time < 0:
            delta_time += 24 * 3600
        return delta_time

    def check_drive_time_violation(self):
        """Sprawdza przekroczenie limitu czasu jazdy."""
        if self.times[TimeType.DRIVE] > 4.5 * 3600:
            self.drive_time_violations += 1

    def check_work_time_violation(self):
        """Sprawdza przekroczenie limitu czasu pracy."""
        if self.times[TimeType.WORK] > 9 * 3600:
            self.work_time_violations += 1

    @staticmethod
    def parse_game_time(game_time):
        """Konwertuje czas ISO 8601 na godziny i minuty."""
        try:
            dt = datetime.strptime(game_time, "%Y-%m-%dT%H:%M:%SZ")
            return dt.hour, dt.minute
        except ValueError:
            return 0, 0

    @staticmethod
    def convert_seconds_to_hh_mm(seconds):
        """Konwertuje sekundy na format godzin i minut."""
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours:02}:{remaining_minutes:02}"
