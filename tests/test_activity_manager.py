import unittest
from modules.activity_manager import ActivityManager

class TestActivityManager(unittest.TestCase):
    def setUp(self):
        self.activity_manager = ActivityManager()

    def test_start_and_stop_activity(self):
        self.activity_manager.start_activity("jazda")
        self.assertEqual(self.activity_manager.current_activity, "jazda")

        self.activity_manager.stop_activity()
        self.assertIsNone(self.activity_manager.current_activity)
        self.assertEqual(len(self.activity_manager.get_log()), 1)

if __name__ == "__main__":
    unittest.main()
