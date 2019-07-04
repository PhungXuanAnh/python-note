import paramiko

class FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)

ssh_conn = FastTransport(('10.0.64.101', 22))
ssh_conn.connect(username='root', password='validium2016')
sftp = paramiko.SFTPClient.from_transport(ssh_conn)
sftp.put()
