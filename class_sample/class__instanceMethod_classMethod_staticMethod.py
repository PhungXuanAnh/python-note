"Reference: https://realpython.com/instance-class-and-static-methods-demystified/"

class MyClass:
    class_attribute1 = "class_attribute1"
    class_attribute2 = "class_attribute2"

    def __init__(self):
        self.instance_attribute1 = "instance_attribute1"

    def __repr__(self):
        return f'Represent about this class instance: ({self.instance_attribute1!r})'

    def instance_method(self):
        print('instance method called: ', self)
        print('instance method can access and modify class attributes: ', self.__class__.class_attribute1)
        print('instance method call static method: ', self.static_method1(self.instance_attribute1))
        print('instance method call class method: ', self.class_method1(self.instance_attribute1))
        print("------------------------------------------------------------")

    # ================================== class method =====================================
    @classmethod
    def class_method(cls):
        print('class method called: ', cls)
        print('class method can access and modify class attributes: ', cls.class_attribute1)
        try:
            cls.instance_attribute1
        except Exception as e:
            print('class method CANNOT access and modify instance attributes: ', e)
        print('class method call static method: ', cls.static_method1(cls.class_attribute1))
        print("------------------------------------------------------------")

    @classmethod
    def class_method1(cls, arg="class method 1 argument"):
        return ("class method 1 called: ", arg)

    # ================================== static method =====================================
    @staticmethod
    def static_method(arg="static method arguments"):
        print('static method called: ', arg)
        print('static method CANNOT access and modify instance or class attributes')
        print("------------------------------------------------------------")

    @staticmethod
    def static_method1(arg="static method 1 arguments"):
        return('static method 1 called: ', arg)


if __name__ == '__main__':
    
    obj = MyClass() # cach goi khac cua instance method
    
    MyClass.instance_method(obj)
    obj.class_method()
    obj.static_method()
    print(obj)

    # MyClass().instance_method()
    # MyClass.class_method()
    # MyClass.static_method()
