import traceback
import sys
from pprint import pprint

# from traceback_example import call_function

def call_function(f, recursion_level=2):
    if recursion_level:
        return call_function(f, recursion_level-1)
    else:
        return f()
# ===================  print_stack ========================
def print_stack_t():
    traceback.print_stack(file=sys.stdout)

print ('Calling f() directly: aaaaaaaaa 1')
print_stack_t()
print
print ('Calling f() from 3 levels deep: aaaaaaaaa 2')
call_function(print_stack_t)

# ===================  format_stack ========================
def format_stack_t():
    return traceback.format_stack()
print ('aaaaaaaaaaa 3')
formatted_stack = call_function(format_stack_t)
pprint(formatted_stack)

# ===================  extract_stack ========================
def extract_stack_t():
    return traceback.extract_stack()
print ('aaaaaaaaaaa 4')
stack = call_function(extract_stack_t)
pprint(stack)
