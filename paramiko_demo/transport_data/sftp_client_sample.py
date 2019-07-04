#!/usr/bin/env python

'''
I’d modify the put/get code to have pipelining (in the new paramiko) 
as this will be extremely slow for large files. Looks very good though 
making the server class..

Tạm dịch: truyền file rất chậm với những file có kích thước lớn, ví dụ:
300M, phải chỉnh lại code của paramiko để có pipeling mới truyền nhanh hơn
'''
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.64.0.169', 
            port=22, 
            username='ubuntu', 
            key_filename='/home/xuananh/.ssh/keypair1.pem'
            )
sftp = ssh.open_sftp()

# push file
sftp.put(localpath='/media/xuananh/data/Temp/Temp.py', 
         remotepath='/home/ubuntu/test100.py')

# pull file
sftp.get(remotepath='/home/ubuntu/test.py',
         localpath='/media/xuananh/data/Temp/Temp000.py')

ssh.close()
print("Done.")

    