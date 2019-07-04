'''
Created on Mar 23, 2017

@author: xuananh
'''

#!/usr/bin/python

from StringIO import StringIO
import paramiko
from scp import SCPClient

class SSHclient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, port, username, password=None, key=None, passphrase=None, key_filename=None):
        '''
        NOTE: 'key_filename' shoudle be ABSOLUTE path, something like: '/home/user/.ssh/key.pem'
              DO NOT use '~/.ssh/key.pem'
        '''
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        self.client.connect(host, port, 
                            username=username, 
                            password=password,
                            key_filename=key_filename,
                            pkey=key, 
                            timeout=self.TIMEOUT)
        self.scp = SCPClient(self.client.get_transport())

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False, get_pty=False):
        '''
        get_pty: True - get tty to run command with sudo
        NOTE: sample to run command in background :
                cmd = 'python script.py > /dev/null 2>&1 &'
        '''
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command, get_pty=get_pty)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(), 
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}
        
    def download_file(self, remote_path, local_path):
        self.scp.get(remote_path, local_path)
        
    def download_dir(self, remote_path, local_path):
        self.scp.get(remote_path, local_path, recursive=True)
        
    def upload_file(self, local_file, remote_path):
        self.scp.put(files=local_file, remote_path=remote_path)
        
    def upload_dir(self, local_dir, remote_path):
        self.scp.put(files=local_dir, remote_path=remote_path, recursive=True)
    
###########################################################################################    

class SshClient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, port, username, password=None, key=None, passphrase=None, key_filename=None):
        '''
        NOTE: 'key_filename' shoudle be ABSOLUTE path, something like: '/home/user/.ssh/key.pem'
              DO NOT use '~/.ssh/key.pem'
        '''
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        self.client.connect(host, port, 
                            username=username, 
                            password=password,
                            key_filename=key_filename,
                            pkey=key, 
                            timeout=self.TIMEOUT)

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False):
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(), 
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

if __name__ == "__main__":
    client = SshClient(host='localhost', 
                       port=22, 
                       username='xuananh', 
                       password='1')

#     client = SshClient(host='10.64.0.169', 
#                        port=22, 
#                        username='ubuntu', 
#                        key_filename='/home/xuananh/.ssh/keypair1.pem')    
    
    try:
        cmd = 'sudo apt-get update'
        ret = client.execute(cmd, sudo=True)
        print ("  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"])
        
        cmd = 'mkdir /root/test'
        print (cmd)
        ret = client.execute(cmd, sudo=True)
        print ("  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"])
    finally:
        client.close() 
