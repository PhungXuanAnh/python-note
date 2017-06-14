#!/usr/bin/env python

import paramiko
import getpass


open('deleteme.txt', 'w').write('you really should delete this]n')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname='10.64.0.169', 
                port=22, 
                username='ubuntu', 
                key_filename='/home/xuananh/.ssh/keypair1.pem'
                )
    sftp = ssh.open_sftp()
    sftp.chdir("/home/ubuntu")
    try:
        print(sftp.stat('/home/ubuntu/test.py'))
        print('file exists')
    except IOError:
        print('copying file...')
        sftp.put(localpath='/media/xuananh/data/Temp/Temp.py', 
                 remotepath='/home/ubuntu/test.py')
    ssh.close()
    print("Done.")
except paramiko.SSHException:
    print("Connection Error")
    
    
  