unittest-sample-test-all:
	.venv/bin/python -m unittest unittest_sample.tests.test_mock_sample

unittest-sample-test-a-case:
	.venv/bin/python -m unittest unittest_sample.tests.test_mock_sample.TestSampleMock.test_get_a_user
