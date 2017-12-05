
# Getting the name of the file without the extension #
import os, getpass
print("1111111111111 " + os.path.splitext("/a/b/c.txt")[0])
print("1111112222222 " + os.path.splitext("/a/b/c.txt")[1])

print("2222222222222 " + os.path.basename("/a/b/c.txt"))
print("3333333333333 " + os.path.splitext(os.path.basename("/a/b/c.txt"))[0])

print("3333334444444 " + os.path.dirname("/a/b/c.txt"))

# get Home Folder
print("4444444444444 " + os.environ.get('HOME'))
# get user name
print("5555555555555 " + os.environ.get('USER'))
# get hostname
import socket
print("6666666666666 " + socket.gethostname())

# get user is running
print ("user id = ", os.getegid())
print ("user_name = ", getpass.getuser())