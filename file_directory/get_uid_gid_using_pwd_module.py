"""
Index    Attribute    Meaning
0    pw_name    The user login name
1    pw_passwd    Encrypted password (optional)
2    pw_uid    User id (integer)
3    pw_gid    Group id (integer)
4    pw_gecos    Comment/full name
5    pw_dir    Home directory
6    pw_shell    Application started on login, usually a command interpreter
"""
from pwd import getpwnam
import os 

print getpwnam(os.environ.get('USER')).pw_uid
print getpwnam(os.environ.get('USER')).pw_gid
# or
print os.getuid()
print os.getgid()

#============================================================== SAMPLE
import pwd

username = os.environ.get('USER')
user_info = pwd.getpwnam(username)

print 'Username:', user_info.pw_name
print 'Password:', user_info.pw_passwd
print 'Comment :', user_info.pw_gecos
print 'UID/GID :', user_info.pw_uid, '/', user_info.pw_gid
print 'Home    :', user_info.pw_dir
print 'Shell   :', user_info.pw_shell

