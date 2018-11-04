"""
Author: Phung Xuan Anh
"""
import unittest
import attendance_system as at
import redis

class UnittestAttendaceSystem(unittest.TestCase):

    dates_valid = [
        {
            "year": 2018,
            "month": 11,
            "day": 3
        },
        {
            "year": 2018,
            "month": 11,
            "day": 4
        }
    ]
    date_invalid_year = {"year": 12018, "month": 11, "day": 4}
    date_invalid_month = {"year": 2018, "month": 15, "day": 4}
    date_invalid_day = {"year": 2018, "month": 11, "day": 50}
    valid_number_user = 100
    invalid_number_user = -1

    def test_get_redis_client(self):
        redis_valid_config = {"host": "localhost", "port": 6379, "db": 1}
        redis_invalid_host = {"host": "1.1.1.1", "port": 6379, "db": 1}
        redis_invalid_port = {"host": "localhost", "port": 63790, "db": 1}
        redis_invalid_db = {"host": "localhost", "port": 6379, "db": 100}
        # pass
        self.assertIsInstance(at.get_redis_client(redis_valid_config), redis.StrictRedis)
        # fail
        self.assertIsNone(at.get_redis_client(redis_invalid_host))
        self.assertIsNone(at.get_redis_client(redis_invalid_port))
        self.assertIsNone(at.get_redis_client(redis_invalid_db))

    def test_generate_binary_string_randomly(self):
        # pass
        self.assertEqual(len(at.generate_binary_string_randomly(self.valid_number_user)), self.valid_number_user)
        # fail
        self.assertIsNone(at.generate_binary_string_randomly(self.invalid_number_user))

    def test_generate_attendance_randomly(self):
        # pass
        self.assertTrue(at.generate_attendance_randomly(self.dates_valid[0], self.valid_number_user))
        # fail
        self.assertFalse(at.generate_attendance_randomly(self.date_invalid_year, self.valid_number_user))
        self.assertFalse(at.generate_attendance_randomly(self.date_invalid_month, self.valid_number_user))
        self.assertFalse(at.generate_attendance_randomly(self.date_invalid_day, self.valid_number_user))
        self.assertFalse(at.generate_attendance_randomly(self.dates_valid[0], self.invalid_number_user))

    def test_get_attendance_a_day(self):
        at.generate_attendance_randomly(self.dates_valid[0], self.valid_number_user)
        # pass
        self.assertIsInstance(at.get_attendance_a_day(self.dates_valid[0], self.valid_number_user), dict)
        # fail
        self.assertIsNone(at.get_attendance_a_day(self.dates_valid[0], self.invalid_number_user))
        self.assertIsNone(at.get_attendance_a_day(self.date_invalid_year, self.valid_number_user))
        self.assertIsNone(at.get_attendance_a_day(self.date_invalid_month, self.valid_number_user))
        self.assertIsNone(at.get_attendance_a_day(self.date_invalid_day, self.valid_number_user))

    def test_get_attendance_consecutive_days(self):
        for date in self.dates_valid:
            at.generate_attendance_randomly(date, self.valid_number_user)
        # pass
        self.assertIsInstance(at.get_attendance_consecutive_days(self.dates_valid[0], self.valid_number_user), dict)
        # fail
        self.assertIsNone(at.get_attendance_consecutive_days(self.dates_valid[0], self.invalid_number_user))
        self.assertIsNone(at.get_attendance_consecutive_days(self.dates_valid[1], self.valid_number_user))
        self.assertIsNone(at.get_attendance_consecutive_days(self.date_invalid_year, self.valid_number_user))
        self.assertIsNone(at.get_attendance_consecutive_days(self.date_invalid_month, self.valid_number_user))
        self.assertIsNone(at.get_attendance_consecutive_days(self.date_invalid_day, self.valid_number_user))

if __name__ == '__main__':
    unittest.main()
