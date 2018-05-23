class MyClass(object):
    def method(self):
        return 'instance method called', self
    
    @classmethod
    def classmethod(cls):
        return 'class method called', cls
    
    @staticmethod
    def staticmethod():
        return 'static method called'
    
    
if __name__ == '__main__':
    obj = MyClass()
    print(obj.method())
    print(MyClass.method(obj))
#     print(MyClass.method()) # error
    
    print(obj.classmethod())
    print(MyClass.classmethod())
    
    print obj.staticmethod()