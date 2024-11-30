"""
run all tests:
    pytest -v unittest_sample/tests/test_mock_sample_pytest.py
run a test:
    pytest -v unittest_sample/tests/test_mock_sample_pytest.py::TestSampleMock::test_get_a_user
run a test with debug:
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client \
        -m pytest -v unittest_sample/tests/test_mock_sample_pytest.py::TestSampleMock::test_add_use_method_2_to_mock

    To debug, see the instruction in these images:
        unittest_sample/tests/debug-mocked-object-1.png
        unittest_sample/tests/debug-mocked-object-2.png
    
NOTE: I decided to use unittest mock instead of pytest mock because there are some reasons make it better
        you can see more here about the discussion between pytest mock and unittest mock:
        https://github.com/pytest-dev/pytest/issues/4576#issuecomment-449864333
        
reference: https://docs.python.org/3/library/unittest.mock.html

the difference between these test with test_mock_sample.py is that I use pytest instead of unittest
in this test, the class didn't inherit from unittest.TestCase
and we use assert instead of self.assert of unittest.TestCase

"""

from unittest import mock

from unittest_sample.app import services

USERNAME, PROPERTIES = "NGUYEN VAN C", "1000 billion USD"
def user_context(arg):
    if arg == "properties":
        return PROPERTIES

    if arg == "another_base_user":
        return mock.Mock(username=USERNAME)


class TestSampleMock():
    @mock.patch("unittest_sample.app.services.User")
    def test_get_a_user(self, mock_User):
        data = "user-1"
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
        
    @mock.patch("unittest_sample.app.services.User.Utility")
    def test_add_use_method_1_to_mock(self, mock_User_Utility):
        data = 3
        mock_User_Utility().add.return_value = data
        result = services.add(1, 2)
        assert result == data
        
    @mock.patch("unittest_sample.app.services.User")
    def test_add_use_method_2_to_mock(self, mock_User):
        data = 3
        mock_User.Utility().add.return_value = data
        result = services.add(1, 2)
        assert result == data

