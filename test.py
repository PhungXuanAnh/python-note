class Stack(object):
    def __init__(self):
        self.stack = []

    def add(self, data):
        if data not in self.stack:
            self.stack.append(data)
            return True
        else:
            return False

    def peek(self):
        return self.stack[0]

    def remove(self):
        if len(self.stack) <= 0:
            return "No element in stack"
        else:
            return self.stack.pop()


aList = [123, 'xyz', 'zara', 'abc']
print("A List : ", aList.pop())
print("B List : ", aList.pop(-2))
