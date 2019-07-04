import paramiko
import datetime
import logging
import sys

class FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)
        
class Transport_SFTP(object):
    """
    Wraps paramiko for super-simple SFTP uploading and downloading.
    """

    def __init__(self, host, username, port=22, password=None, pkey=None):

#         self.transport = paramiko.Transport((host, port))
        self.transport = FastTransport((host, port))
        
        if password is not None:
            self.transport.connect(username=username, password=password)
        elif pkey is not None:
            pkey = paramiko.RSAKey.from_private_key_file(pkey)
            self.transport.connect(username=username, pkey=pkey)
        else:
            raise IOError("Password or Private-Key should be provided")
            
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def upload(self, local, remote):
        logging.info("Uploading file...")
        start = datetime.datetime.now()
        
        self.sftp.put(local, remote)
        
        now = datetime.datetime.now()
        logging.info("Time to upload: {} seconds".format((now - start).seconds))

    def download(self, remote, local):
        logging.info("Downloading file...")
        start = datetime.datetime.now()
        
        self.sftp.get(remote, local)
        
        now = datetime.datetime.now()
        logging.info("Time to download: {} seconds".format((now - start).seconds))

    def close(self):
        """
        Close the connection if it's active
        """

        if self.transport.is_active():
            self.sftp.close()
            self.transport.close()

    # with-statement support
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
        
        
if __name__ == '__main__':
    logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S", 
    stream=sys.stdout,
    )
    
#     trans = Transport_SFTP(host='10.64.0.169',
#                           username='ubuntu',
#                           pkey='/home/xuananh/.ssh/keypair1.pem')
#     
#     trans.download(remote='/home/ubuntu/test.py', 
#                    local='/media/xuananh/data/Temp/test222.py')
#     
#     trans.upload(local='/media/xuananh/data/Temp/Temp (copy).py', 
#                  remote='/home/ubuntu/testaaa.py')
#     trans.close()
    trans = Transport_SFTP(host='10.64.0.101',
                          username='root',
                          password='validium2016')
    
    # openssh client: 00:36
    # paramiko.Transport: Time to upload: 81 seconds
    # FastTransport: Time to upload: 81 seconds
    
    trans.upload(local='/media/xuananh/data/Downloads/Saved/Softwares/xmind-linux-3.5.3.201506180105_amd64.deb', 
                 remote='/root/test/xmind2.deb')
    trans.close()
    
    