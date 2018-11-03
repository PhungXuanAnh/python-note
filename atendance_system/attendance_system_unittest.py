import unittest
import attendance_system as at
import redis


class UnittestAttendaceSystem(unittest.TestCase):

    def test_pass_get_redis_client(self):
        r_client = at.get_redis_client()
        self.assertIsInstance(r_client, redis.StrictRedis)

    def test_fail_get_redis_client(self):
        r_client = at.get_redis_client(host="1.1.1.1")
        self.assertEqual(r_client, None)
        r_client = at.get_redis_client(port=1234)
        self.assertEqual(r_client, None)
        r_client = at.get_redis_client(db=20)
        self.assertEqual(r_client, None)


if __name__ == '__main__':
    unittest.main()
