import unittest
import bit_string_redis as bt


class TestBitString(unittest.TestCase):
    def test_init_user(self):
        size = len(bt.init_user_ids())
        self.assertEqual(size, bt.USERS)

    def test_init_user_less_than_zero(self):
        bt.USERS = -1
        size = len(bt.init_user_ids())
        self.assertEqual(size, 0)

    #pass case
    def test_pass_init_data_a_day(self):
        bt.USERS = 100
        day = 'test'
        user_ids = bt.init_user_ids()
        self.assertTrue(bt.init_data_a_day(user_ids, day))

    # fail case
    def test_fail_init_data_a_day(self):
        user_ids = bt.init_user_ids()
        self.assertFalse(bt.init_data_a_day(user_ids, None))
        self.assertFalse(bt.init_data_a_day(user_ids, ""))
        self.assertFalse(bt.init_data_a_day(None, ""))
        self.assertFalse(bt.init_data_a_day([], None))
        self.assertFalse(bt.init_data_a_day([], ""))

    def test_present_users_a_day(self):
        day = "test"
        user_ids = bt.init_user_ids()
        # pass
        self.assertGreater(len(bt.get_present_users_a_day(user_ids, day)), -1)
        # fail
        self.assertEqual(bt.get_present_users_a_day(user_ids, None), None)
        self.assertEqual(bt.get_present_users_a_day(user_ids, ""), None)
        self.assertEqual(bt.get_present_users_a_day(None, day), None)
        self.assertEqual(bt.get_present_users_a_day(None, None), None)
        self.assertEqual(bt.get_present_users_a_day([], None), None)

    def test_absent_users_a_day(self):
        day = "test"
        user_ids = bt.init_user_ids()
        #pass
        self.assertGreater(len(bt.get_absent_users_a_day(user_ids, day)), -1)
        #fail
        self.assertEqual(bt.get_absent_users_a_day(user_ids, None), None)
        self.assertEqual(bt.get_absent_users_a_day(user_ids, ""), None)
        self.assertEqual(bt.get_absent_users_a_day(None, day), None)
        self.assertEqual(bt.get_absent_users_a_day(None, None), None)
        self.assertEqual(bt.get_absent_users_a_day([], None), None)

    def test_present_users_consecutive_days(self):
        user_ids = bt.init_user_ids()
        bt.init_data_a_day(user_ids, 'day1')
        bt.init_data_a_day(user_ids, 'day2')
        keys = ['day1', 'day2']
        #pass
        self.assertGreater(len(bt.present_users_consecutive_days(user_ids, keys)), -1)

        #fail
        self.assertEqual(bt.present_users_consecutive_days(user_ids, None), None)
        self.assertEqual(bt.present_users_consecutive_days(user_ids, []), None)
        self.assertEqual(bt.present_users_consecutive_days(None, keys), None)
        self.assertEqual(bt.present_users_consecutive_days([], keys), None)
        self.assertEqual(bt.present_users_consecutive_days(None, None), None)
        self.assertEqual(bt.present_users_consecutive_days([], []), None)
        self.assertEqual(bt.present_users_consecutive_days(user_ids, "abc"), None)
        self.assertEqual(bt.present_users_consecutive_days(None, "abc"), None)
        self.assertEqual(bt.present_users_consecutive_days([], "abc"), None)

    def test_absent_users_consecutive_days(self):
        user_ids = bt.init_user_ids()
        bt.init_data_a_day(user_ids, 'day1')
        bt.init_data_a_day(user_ids, 'day2')
        keys = ['day1', 'day2']
        #pass
        self.assertGreater(len(bt.absent_users_consecutive_days(user_ids, keys)), -1)

        #fail
        self.assertEqual(bt.absent_users_consecutive_days(user_ids, None), None)
        self.assertEqual(bt.absent_users_consecutive_days(user_ids, []), None)
        self.assertEqual(bt.absent_users_consecutive_days(None, keys), None)
        self.assertEqual(bt.absent_users_consecutive_days([], keys), None)
        self.assertEqual(bt.absent_users_consecutive_days(None, None), None)
        self.assertEqual(bt.absent_users_consecutive_days([], []), None)
        self.assertEqual(bt.absent_users_consecutive_days(user_ids, "abc"), None)
        self.assertEqual(bt.absent_users_consecutive_days(None, "abc"), None)
        self.assertEqual(bt.absent_users_consecutive_days([], "abc"), None)


    def test_present_users_consecutive_days_with_large_user(self):
        bt.USERS = 100000
        user_ids = bt.init_user_ids()
        bt.init_data_a_day(user_ids, 'day1')
        bt.init_data_a_day(user_ids, 'day2')
        keys = ['day1', 'day2']
        # pass
        self.assertGreater(len(bt.absent_users_consecutive_days(user_ids, keys)), -1)

    def test_absent_users_consecutive_days_with_large_user(self):
        user_ids = bt.init_user_ids()
        bt.init_data_a_day(user_ids, 'day1')
        bt.init_data_a_day(user_ids, 'day2')
        keys = ['day1', 'day2']
        #pass
        self.assertGreater(len(bt.absent_users_consecutive_days(user_ids, keys)), -1)



if __name__ == '__main__':
    unittest.main()
