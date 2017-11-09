'''
Created on Jul 28, 2017

@author: xuananh
'''
class Foo(object):
    pass
  
foo = Foo()
foo.a = 3
Foo.b = property(lambda self: self.a + 1)
print foo.b