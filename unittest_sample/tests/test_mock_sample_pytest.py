# to run test:
# cd python-note
# pytest -v unittest_sample/tests/test_mock_sample_pytest.py
from unittest import mock
from unittest_sample.app import services
# reference: https://docs.python.org/3/library/unittest.mock.html
# why use unittest mock instead of pytest mock: https://github.com/pytest-dev/pytest/issues/4576#issuecomment-449864333

USERNAME, PROPERTIES = "NGUYEN VAN C", "1000 billion USD"
def user_context(arg):
    if arg == "properties":
        return PROPERTIES

    if arg == "another_base_user":
        return mock.Mock(username=USERNAME)

class TestSampleMock():
    @mock.patch("unittest_sample.app.services.User")
    def test_get_a_user(self, mock_User):
        data = ""
        mock_User.objects.get.return_value = data
        result = services.get_a_user()
        assert result == data

    @mock.patch("unittest_sample.app.services.User")
    def test_count_user(self, mock_User):
        data = 1
        mock_User.objects.return_value.count.return_value = data
        result = services.count_users()
        assert result == data

    @mock.patch("unittest_sample.app.services.User")
    def test_get_user_name(self, mock_User):
        data = 'nguyen van a'
        mock_User.return_value.get_name.return_value = data
        result = services.get_user_name()
        assert result == data

    @mock.patch("unittest_sample.app.services.User.context")
    def test_get_another_base_user_name_and_his_properties(self, mock_User_context):
        data = 'nguyen van a'
        mock_User_context.get = mock.Mock(side_effect=user_context)
        name, properties = services.get_another_base_user_name_and_his_properties()
        assert name == USERNAME
        assert properties == PROPERTIES

