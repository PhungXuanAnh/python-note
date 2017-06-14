import paramiko
import logging
import datetime
import sys
from scp import SCPClient

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S", 
    stream=sys.stdout,
    )

local_file = '/media/xuananh/data/Temp/test3.py'
remote_file = '/home/ubuntu/test.py'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.64.0.101', 
            port=22, 
            username='root', 
            password='validium2016'
            )

scp = SCPClient(ssh.get_transport())

"""
Transfer files from remote host to localhost

@param remote_path: path to retreive from remote host. since this is
    evaluated by scp on the remote host, shell wildcards and
    environment variables may be used.
@type remote_path: str
@param local_path: path in which to receive files locally
@type local_path: str
@param recursive: transfer files and directories recursively
@type recursive: bool
@param preserve_times: preserve mtime and atime of transfered files
    and directories.
@type preserve_times: bool
"""
# scp.get(remote_path, local_path, recursive, preserve_times)
# scp.get(remote_path='/home/ubuntu/test.py', 
#         local_path='/media/xuananh/data/Temp/test3.py')

logging.info("Dowloading file...")
start = datetime.datetime.now()

scp.get(remote_path='/root/test/agentworker', 
        local_path='/media/xuananh/data/Temp/',
        recursive=True)

now = datetime.datetime.now()
logging.info("Time to download: {} seconds".format((now - start).seconds))

"""
Transfer files to remote host.

@param files: A single path, or a list of paths to be transfered.
    recursive must be True to transfer directories.
@type files: string OR list of strings
@param remote_path: path in which to receive the files on the remote
    host. defaults to '.'
@type remote_path: str
@param recursive: transfer files and directories recursively
@type recursive: bool
@param preserve_times: preserve mtime and atime of transfered files
    and directories.
@type preserve_times: bool
"""
# scp.put(files, remote_path, recursive, preserve_times)

# 33s
logging.info("Uploading file...")
start = datetime.datetime.now()
 
# scp.put(files='/media/xuananh/data/Downloads/Saved/Softwares/xmind-linux-3.5.3.201506180105_amd64.deb', 
#         remote_path='/root/test/xmind6.deb')
scp.put(files='/media/xuananh/data/Dropbox/Viosoft/Eclipse_workspace/Validium/validium/agentworker', 
        remote_path='/root/test/',
        recursive=True)
 
now = datetime.datetime.now()
logging.info("Time to upload: {} seconds".format((now - start).seconds))

scp.close()
ssh.close()