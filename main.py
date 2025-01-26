from threading import Thread
from modules.telemetry_manager import TelemetryManager
from gui.main_gui import TachographGUI
from gui.overlay_gui import OverlayGUI
import sys

def global_exception_hook(exctype, value, traceback):
    print(f"Nieobsłużony wyjątek: {value}")
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = global_exception_hook

def main():
    print("Uruchamianie ETS2 Tachograph z GUI i nakładką...")

    # Adres serwera telemetrycznego
    server_url = "http://localhost:25555/api/ets2/telemetry"

    # Inicjalizacja menedżera telemetrycznego
    telemetry_manager = TelemetryManager(server_url)

    # Funkcja uruchamiająca GUI
    def run_full_gui():
        gui = TachographGUI(telemetry_manager)
        gui.run()

    # Funkcja uruchamiająca nakładkę
    def run_overlay():
        overlay = OverlayGUI(telemetry_manager)
        overlay.run()

    # Uruchom pełne GUI i nakładkę w osobnych wątkach
    gui_thread = Thread(target=run_full_gui)
    overlay_thread = Thread(target=run_overlay)

    gui_thread.start()
    overlay_thread.start()

    gui_thread.join()
    overlay_thread.join()

if __name__ == "__main__":
    main()
