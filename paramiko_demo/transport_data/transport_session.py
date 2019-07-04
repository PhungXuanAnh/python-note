import paramiko
import getpass

pw = getpass.getpass()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def start():
    try :
        client.connect('127.0.0.1', port=22, username='xuananh', password=pw)
        return True
    except Exception as e:
        #client.close()
        print(e)
        return False

while start():
    key = True
    cmd = raw_input("Command to run: ")
    if cmd == "":
        break
    session = client.get_transport().open_session()
    print("running '%s'" % cmd)
    session.exec_command(cmd)
    while key:
        if session.recv_ready():
            print("recv:\n%s" % session.recv(4096).decode('ascii'))
        if session.recv_stderr_ready():
            print("error:\n%s" % session.recv_stderr(4096).decode('ascii'))
        if session.exit_status_ready():
            print("exit status: %s" % session.recv_exit_status())
            key = False
            client.close()
client.close()