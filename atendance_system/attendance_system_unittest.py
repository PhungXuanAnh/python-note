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
        # pass
        at.generate_attendance_randomly(2010, 10, 10, 100)
        self.assertIsInstance(at.get_attendance_a_day(2010, 10, 10, 100), dict)
        # fail
        self.assertEqual(at.get_attendance_a_day(2010, 10, 10, -1), None)
        self.assertEqual(at.get_attendance_a_day(12010, 10, 10, 100), None)
        self.assertEqual(at.get_attendance_a_day(2010, 15, 10, 100), None)
        self.assertEqual(at.get_attendance_a_day(2010, 10, 0, 100), None)

if __name__ == '__main__':
    unittest.main()
