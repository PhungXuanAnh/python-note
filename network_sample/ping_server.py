def check_ping_server():
    import shlex
    import subprocess
    
    # Tokenize the shell command
    # cmd will contain  ["ping","-c1","google.com"]
         
    # cmd=shlex.split("ping -c1 google.com")
    cmd=shlex.split("ping -c1 10.64.0.182")
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        #Will print the command failed with its exit status
        print ("The IP {0} is Not Reachable".format(cmd[-1]))
    else:
        print ("The IP {0} is Reachable".format(cmd[-1]))
        
check_ping_server()
        
        