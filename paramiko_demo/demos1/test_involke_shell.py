# import workflow
# import console
import paramiko
import time

strComputer = 'localhost'
strUser = 'xuananh'
strPwd = '1'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=strComputer, username=strUser, password=strPwd)

channel = client.invoke_shell()
# channel.send('ls -lha --color=never\n')
channel.send('top \n')
time.sleep(3)
output=channel.recv(2024)
print(output)

#Close the connection
client.close()
print('Connection closed.')