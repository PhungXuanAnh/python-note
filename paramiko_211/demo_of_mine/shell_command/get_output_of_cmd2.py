#!/usr/bin/env python
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ssh.connect(hostname='10.64.0.169', 
#             port=22, 
#             username='ubuntu', 
#             key_filename='/home/xuananh/.ssh/keypair1.pem'
#             )
ssh.connect(hostname='localhost', 
            port=22, 
            username='xuananh', 
            password='1'
            )

print('Connected')

remote_conn = ssh.invoke_shell()

# remote_conn.send('ls -la ~/ \n')
# remote_conn.send('sudo mkdir /root/test\n')
# remote_conn.send('sudo apt-get update \n ls -la ~/ \n find \n')
remote_conn.send('sudo apt-get update \n')
remote_conn.send('1\n')
time.sleep(2)

while remote_conn.recv_ready():
    time.sleep(1)
    print (remote_conn.recv(1024))

print (remote_conn.recv_ready())
remote_conn.send('exit\n')
if remote_conn.exit_status_ready():
    print (remote_conn.recv_exit_status())
