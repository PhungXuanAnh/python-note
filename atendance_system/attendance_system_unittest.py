import unittest
import attendance_system as at
import redis


class UnittestAttendaceSystem(unittest.TestCase):

    def test_get_redis_client(self):
        # pass
        r_client = at.get_redis_client()
        self.assertIsInstance(r_client, redis.StrictRedis)
        # fail
        r_client = at.get_redis_client(host="1.1.1.1")
        self.assertEqual(r_client, None)
        r_client = at.get_redis_client(port=1234)
        self.assertEqual(r_client, None)
        r_client = at.get_redis_client(db=20)
        self.assertEqual(r_client, None)

    def test_generate_attendance_randomly(self):
        # pass
        self.assertTrue(at.generate_attendance_randomly(2011, 1, 1, 100))
        # fail
        self.assertFalse(at.generate_attendance_randomly(-2018, 1, 1, 100))
        self.assertFalse(at.generate_attendance_randomly(2018, 15, 1, 100))
        self.assertFalse(at.generate_attendance_randomly(2018, 1, 100, 100))
        self.assertFalse(at.generate_attendance_randomly(2018, 1, 1, 0))

    def test_get_attendance_a_day(self):
        at.generate_attendance_randomly(2010, 10, 10, 100)
        # pass
        self.assertIsInstance(at.get_attendance_a_day(2010, 10, 10, 100), dict)
        # fail
        self.assertIsNone(at.get_attendance_a_day(2010, 10, 10, -1))
        self.assertIsNone(at.get_attendance_a_day(12010, 10, 10, 100))
        self.assertIsNone(at.get_attendance_a_day(2010, 15, 10, 100))
        self.assertIsNone(at.get_attendance_a_day(2010, 10, 0, 100))

    def test_get_attendance_consecutive_days(self):
        NUMBER_USERS = 100
        dates = [
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
        for date in dates:
            at.generate_attendance_randomly(date["year"], date["month"], date["day"], NUMBER_USERS)
        # pass
        self.assertIsInstance(at.get_attendance_consecutive_days(dates[0], NUMBER_USERS), dict)
        # fail
        self.assertIsNone(at.get_attendance_consecutive_days(dates[1], NUMBER_USERS))
        self.assertIsNone(at.get_attendance_consecutive_days({"year": 20091, "month": 1, "day": 2}, NUMBER_USERS))
        self.assertIsNone(at.get_attendance_consecutive_days({"year": 2009, "month": 21, "day": 2}, NUMBER_USERS))
        self.assertIsNone(at.get_attendance_consecutive_days({"year": 2009, "month": 1, "day": 92}, NUMBER_USERS))
        self.assertIsNone(at.get_attendance_consecutive_days({"year": 20091, "month": 1, "day": 1}, -100))


if __name__ == '__main__':
    unittest.main()
