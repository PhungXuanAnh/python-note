
def timeout_command(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    
    import subprocess, datetime, os, time, signal
    
    start = datetime.datetime.now()
    process = subprocess.Popen(command, 
                               shell=True,
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               preexec_fn=os.setsid)
    print("Start process with PID = {}".format(process.pid))
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            print('Timeout happend')
            os.killpg(os.getpgid(process.pid + 1), signal.SIGTERM)
    return process.stdout.read(), process.poll()



# print timeout_command(["sleep", "3"], 2)
# print timeout_command(["sleep", "1"], 2)
mypass = '1'
cmd1 = 'apt-get update'
cmd = "echo %s | sudo -S %s" % (mypass, cmd1)
# print timeout_command(cmd, 2)
timeout_command('ping 8.8.8.8', 10)
