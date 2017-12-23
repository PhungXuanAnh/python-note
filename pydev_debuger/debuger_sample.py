'''
Created on Dec 20, 2017

@author: xuananh
'''

class Test(object):
    
    def method(self,i):
        if i < 10:
            print(i)
            i += 1
            self.method(i)
            
if __name__ == '__main__':
    Test().method(0)