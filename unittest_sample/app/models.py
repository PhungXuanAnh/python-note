class BaseUser(object):
    username = "nguyen van a"
    email = "abc@gmail.com"

    def __init__(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email

    @classmethod
    def get(cls, arg):
        if arg == "username":
            return "base user username: {}".format(cls.username)
        elif arg == "email":
            return "base user email: {}".format(cls.email)
        else:
            return "count of base user: {} --- {}".format(cls.username, cls.email)

    def count(self):
        return "count of base user: 123"



class User:
    objects = BaseUser
    context = {
        "properties": "1 billion usd",
        "another_base_user": BaseUser("nguyen van b", "b@gmail.com")
    }

    def get_name(self):
        return self.username


if __name__ == "__main__":
    print(User.objects)
    print(User.objects.get("username"))
    print(User.objects("Nguyen Van A", "a@gmail.com").count())
    print(User.context.get("is_rich"))
    print(User.context.get("another_base_user").username)