from .models import User

"""
    We will learn how to mock all the ways to call User in file: unittest_sample/tests/test_mock_sample.py
"""

def get_a_user():
    return User.objects.get("1")

def count_users():
    return User.objects("Nguyen Van A", "a@gmail.com").count()

def get_user_name():
    user = User()
    return user.get_name()