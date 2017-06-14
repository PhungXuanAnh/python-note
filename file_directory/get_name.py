
# Getting the name of the file without the extension #
import os, getpass
print(os.path.splitext("/a/b/c.txt")[0])

from os.path import basename
print(basename("/a/b/c.txt"))
print(basename("'~/.validium/keypair/yardstick_key-453944d3"))


# get Home Folder
print os.environ.get('HOME')
# get user name
print os.environ.get('USER')
# get hostname
import socket
print socket.gethostname()

# get user is running
print ("user id = ", os.getegid())
print ("user_name = ", getpass.getuser())