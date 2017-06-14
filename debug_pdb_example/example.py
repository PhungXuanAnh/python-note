'''
 Execute the next statement with 'n' (next)
 Repeating the last debugging command with ENTER
 Quitting it all with 'q' (quit)
 Printing the value of variables with 'p' (print)
 Turning off the (Pdb) prompt with 'c' (continue)
 Seeing where you are with 'l' (list)
 
 Stepping into subroutines with 's' (step into subroutine or sub function)
 
'''
import pdb
a = "aaa"
pdb.set_trace()
b = "bbb"
c = "ccc"
final = a + b + c
print final
  
# from test.test import TestClass
# 
# t1 = TestClass()
# t1.test_method("aaaaaaaaaaaaaaa")
  
from test.test import Test
test = Test()
test.print_a()
test.raise_erro()
print("AAAAAAAAAAAAAAAA")
test.print_b()

# import pdb
#   
# def combine(s1,s2):      # define subroutine combine, which...
#     s3 = s1 + s2 + s1    # sandwiches s2 between copies of s1, ...
#     s3 = '"' + s3 +'"'   # encloses it in double quotes,...
#     return s3            # and returns it.
# 
# a = "aaa"
# # pdb.set_trace()
# b = "bbb"
# c = "ccc"
# final = combine(a,b)
# print final


