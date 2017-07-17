import shlex

#    JOIN
# The Python join() method is a string method, and takes a list of things to join with the string
separator = "-";
seq = ("a", "b", "c"); # This is sequence of strings.
# seq = ("a")
print separator.join( seq )
# return: a-b-c

a = "this is a string"
a = "-".join(a) # in this case a was treated as list ['t', 'h', 'i', 's', ' ', 'i', 's', ' ', ...]
print a
# t-h-i-s- -i-s- -a- -s-t-r-i-n-g

print ",".join(["a", "b", "c"])
# 'a,b,c'

 
#   SPLIT
a = "this is a string"
a = a.split(" ") # a is converted to a list of strings. 
print a
# ['this', 'is', 'a', 'string']


# inputString.split('\n')  # --> ['Line 1', 'Line 2', 'Line 3']
# inputString.splitlines(True)  # --> ['Line 1\n', 'Line 2\n', 'Line 3']

print shlex.split("ping -c1 8.8.8.8")

print "a-b-c".split("-")
print "a-b-c".split("-")[0]

