import requests

class TelemetryManager:
    def __init__(self, server_url):
        self.server_url = server_url

    def fetch_telemetry_data(self):
        """Pobiera dane telemetryczne z serwera."""
        try:
            response = requests.get(self.server_url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            print("Błąd: Timeout przy połączeniu z serwerem telemetrycznym.")
        except requests.RequestException as e:
            print(f"Błąd: {e}")
        return {}
