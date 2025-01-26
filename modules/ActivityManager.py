class ActivityManager:
    def __init__(self):
        self.current_activity = None
        self.activity_log = []

    def start_activity(self, activity_type):
        """Rozpoczyna nową aktywność."""
        self.current_activity = activity_type
        print(f"Rozpoczęto aktywność: {activity_type}.")

    def stop_activity(self):
        """Kończy bieżącą aktywność."""
        if self.current_activity:
            self.activity_log.append(self.current_activity)
            print(f"Zakończono aktywność: {self.current_activity}.")
            self.current_activity = None

    def get_log(self):
        """Zwraca historię aktywności."""
        return self.activity_log
