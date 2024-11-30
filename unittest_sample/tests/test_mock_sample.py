"""
test all case:
    cd python-note
    .venv/bin/python -m unittest -vv unittest_sample.tests.test_mock_sample
test a case:
    cd python-note
    .venv/bin/python -m unittest unittest_sample.tests.test_mock_sample.TestSampleMock.test_get_a_user
"""

from unittest import TestCase, mock

from unittest_sample.app import services

USERNAME, PROPERTIES = "NGUYEN VAN C", "1000 billion USD"
def user_context(arg):
    if arg == "properties":
        return PROPERTIES

    if arg == "another_base_user":
        return mock.Mock(username=USERNAME)

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

    @mock.patch("unittest_sample.app.services.User.context")
    def test_get_another_base_user_name_and_his_properties(self, mock_User_context):
        data = 'nguyen van a'
        mock_User_context.get = mock.Mock(side_effect=user_context)
        name, properties = services.get_another_base_user_name_and_his_properties()
        self.assertEqual(name, USERNAME)
        self.assertEqual(properties, PROPERTIES)

