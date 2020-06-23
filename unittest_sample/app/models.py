class BaseUser(object):
    username = "abc"
    email = "abc@gmail.com"

    def __init__(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email

    @classmethod
    def get(cls, arg):
        return "get of base user: {}".format(arg)

    def count(self):
        return "count of base user: {} --- {}".format(self.username, self.email)



class User:
    objects = BaseUser

    def get_name(self):
        return self.username


if __name__ == "__main__":
    print(User.objects)
    print(User.objects.get("1"))
    print(User.objects("Nguyen Van A", "a@gmail.com").count())