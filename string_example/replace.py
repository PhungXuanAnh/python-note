sample_string = "192.168.0.1"

print sample_string.replace(".","_")

Fname = "John"
Lname = "Doe"
Age = "24"


# PYTHON 2
test1 = '%s is %s years old' % ("Mar", "1")
print test1


# PYTHON 3
print '{} {} is {} years old.'.format(Fname, Lname, Age)

print '{0} {1} is {2} years old.'.format(Fname, Lname, Age)

print '{0} {1} is {0} years old.'.format(Fname, Lname, Age)

test = "aaaaaaaa {}".format("bbbbbbb")
print (test)