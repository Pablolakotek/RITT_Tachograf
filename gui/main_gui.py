import tkinter as tk
from gui.gui_elements import create_label, create_quit_button, create_warning_label, create_time_and_violation_row
from modules.time_manager import TimeManager, TimeType
from modules.telemetry_manager import TelemetryManager

class TachographGUI:
    def __init__(self, telemetry_manager):
        self.telemetry_manager = telemetry_manager
        self.time_manager = TimeManager()
        self.last_game_time = None

        self.root = tk.Tk()
        self.root.title("ETS2 Tachograph")
        self.root.geometry("800x700")

        self.labels = {}
        self.create_widgets()
        self.monitor_telemetry()

    def run(self):
        """Uruchamia główną pętlę Tkintera."""
        self.root.mainloop()

    def create_widgets(self):
        self.labels["status"] = create_label(self.root, "Status: brak danych")
        self.warning_label = create_warning_label(self.root)

        # Czas jazdy i przekroczenia
        self.labels["drive_time"], self.labels["drive_time_violations"] = create_time_and_violation_row(
            self.root, "Czas jazdy: 00:00", "Przekroczenia: 0"
        )
        # Czas pracy i przekroczenia
        self.labels["work_time"], self.labels["work_time_violations"] = create_time_and_violation_row(
            self.root, "Czas pracy: 00:00", "Przekroczenia: 0"
        )
        # Pozostałe informacje
        self.labels["break_time"] = create_label(self.root, "Czas przerw: 00:00")
        self.labels["break_remaining"] = create_label(self.root, "Pozostały czas przerwy: 00:00")
        self.labels["game_time"] = create_label(self.root, "Czas gry: brak danych")
        self.labels["speed"] = create_label(self.root, "Prędkość pojazdu: 0 km/h")

        self.quit_button = create_quit_button(self.root, self.on_close)
        self.quit_button.pack(pady=10)

    def monitor_telemetry(self):
        """Monitoruje dane telemetryczne i aktualizuje GUI."""
        try:
            telemetry_data = self.telemetry_manager.fetch_telemetry_data()

            if not telemetry_data:
                self.warning_label.config(text="Brak danych z gry. Upewnij się, że serwer telemetryczny działa.")
                return

            # Pobieranie czasu gry
            game_time_raw = telemetry_data.get("game", {}).get("time", "Brak danych")
            if game_time_raw != "Brak danych":
                game_hours, game_minutes = self.time_manager.parse_game_time(game_time_raw)
                self.labels["game_time"].config(text=f"Czas gry: {game_hours:02}:{game_minutes:02}")

                # Aktualizacja czasów
                current_game_time = game_hours * 3600 + game_minutes * 60
                if self.last_game_time is not None:
                    delta_time = self.time_manager.calculate_delta_time(current_game_time, self.last_game_time)

                    if telemetry_data.get("truck", {}).get("engineOn", False):
                        if telemetry_data.get("truck", {}).get("speed", 0) > 0:
                            self.time_manager.times[TimeType.DRIVE] += delta_time
                            self.time_manager.times[TimeType.WORK] += delta_time
                            self.time_manager.check_drive_time_violation()
                        else:
                            self.time_manager.times[TimeType.WORK] += delta_time
                    else:
                        self.time_manager.times[TimeType.BREAK] += delta_time
                        if self.time_manager.break_remaining_time > 0:
                            self.time_manager.break_remaining_time -= delta_time

                    self.time_manager.check_work_time_violation()

                self.last_game_time = current_game_time

            # Aktualizacja GUI
            self.update_gui(telemetry_data)

            # Wywołanie ponowne po 1 sekundzie
            self.root.after(1000, self.monitor_telemetry)
        except Exception as e:
            self.warning_label.config(text=f"Błąd podczas monitorowania: {e}")
            print(f"Błąd podczas monitorowania: {e}")

    def update_gui(self, telemetry_data):
        """Aktualizuje wartości wyświetlane w GUI."""
        self.labels["drive_time"].config(
            text=f"Czas jazdy: {self.time_manager.convert_seconds_to_hh_mm(self.time_manager.times[TimeType.DRIVE])}"
        )
        self.labels["work_time"].config(
            text=f"Czas pracy: {self.time_manager.convert_seconds_to_hh_mm(self.time_manager.times[TimeType.WORK])}"
        )
        self.labels["break_time"].config(
            text=f"Czas przerw: {self.time_manager.convert_seconds_to_hh_mm(self.time_manager.times[TimeType.BREAK])}"
        )
        self.labels["break_remaining"].config(
            text=f"Pozostały czas przerwy: {self.time_manager.convert_seconds_to_hh_mm(self.time_manager.break_remaining_time)}"
        )

        # Aktualizacja liczników przekroczeń
        self.labels["drive_time_violations"].config(text=f"Przekroczenia: {self.time_manager.drive_time_violations}")
        self.labels["work_time_violations"].config(text=f"Przekroczenia: {self.time_manager.work_time_violations}")

        # Prędkość i paliwo
        truck_data = telemetry_data.get("truck", {})
        speed = int(truck_data.get("speed", 0))  # Zaokrąglenie prędkości
        fuel = truck_data.get("fuel", 0)
        self.labels["speed"].config(text=f"Prędkość pojazdu: {speed} km/h")
        self.labels["status"].config(text=f"Poziom paliwa: {fuel:.1f} litrów")

    def on_close(self):
        """Zamyka aplikację."""
        self.root.quit()
        self.root.destroy()
