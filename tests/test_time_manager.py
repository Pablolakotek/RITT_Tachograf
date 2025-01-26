import unittest
from modules.time_manager import TimeManager, TimeType

class TestTimeManager(unittest.TestCase):
    def setUp(self):
        self.time_manager = TimeManager()

    def test_calculate_delta_time(self):
        delta = self.time_manager.calculate_delta_time(100, 50)
        self.assertEqual(delta, 50)

    def test_drive_time_violation(self):
        self.time_manager.times[TimeType.DRIVE] = 5 * 3600
        self.time_manager.check_drive_time_violation()
        self.assertEqual(self.time_manager.drive_time_violations, 1)

    def test_convert_seconds_to_hh_mm(self):
        formatted_time = self.time_manager.convert_seconds_to_hh_mm(3661)
        self.assertEqual(formatted_time, "01:01")

if __name__ == "__main__":
    unittest.main()
