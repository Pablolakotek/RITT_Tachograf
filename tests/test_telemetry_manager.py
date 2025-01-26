import unittest
from modules.telemetry_manager import TelemetryManager

class TestTelemetryManager(unittest.TestCase):
    def setUp(self):
        self.telemetry_manager = TelemetryManager("http://localhost:25555/api/ets2/telemetry")

    def test_fetch_telemetry_data(self):
        data = self.telemetry_manager.fetch_telemetry_data()
        self.assertIsInstance(data, dict)

if __name__ == "__main__":
    unittest.main()
