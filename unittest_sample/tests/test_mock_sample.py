# to run test:
# cd python-note
# make unittest-sample-test-all
from unittest import mock, TestCase
from unittest_sample.app import services


class TestSampleMock(TestCase):
    @mock.patch("unittest_sample.app.services.User")
    def test_get_a_user(self, mock_User):
        data = ""
        mock_User.objects.get.return_value = data
        result = services.get_a_user()
        self.assertEqual(result, data, result)

    @mock.patch("unittest_sample.app.services.User")
    def test_count_user(self, mock_User):
        data = 1
        mock_User.objects.return_value.count.return_value = data
        result = services.count_users()
        self.assertEqual(result, data, result)

    @mock.patch("unittest_sample.app.services.User")
    def test_get_user_name(self, mock_User):
        data = 'nguyen van a'
        mock_User.return_value.get_name.return_value = data
        result = services.get_user_name()
        self.assertEqual(result, data, result)

