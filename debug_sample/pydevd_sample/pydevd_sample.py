'''
################## VERY IMPORTANCE ###################
NOTE 1: when remote debug flask in multiproces,
        it must set app.run(debug=False)
        
NOTE 2: cac buoc test khi khong the ket noi den debug server
        1. debug file nay voi breakpoint 
        2. debug file nay voi pydevd.settrace() va debug server tren local
        3. telnet
        4. debug file nay voi pydevd.settrace() va debug server tren remote
'''


import multiprocessing

def worker():
    var1 = 4
    while var1 < 6:
        import pydevd;pydevd.settrace(host="10.80.0.101",
                                      port=5678,
                                      stdoutToServer=True,
                                      stderrToServer=True,
                                      )

        import pydevd;pydevd.settrace()
        
        var1 = var1 + 1
        print var1
    
    
if __name__ == '__main__':
    '''
    run on remote machine and local machine: pip install pydevd
    '''
    # khong duoc thi chay thu dong duoi
    # /home/ubuntu/.validium-env/lib/python2.7/site-packages/pydevd_file_utils.py
    # /usr/local/lib/python2.7/dist-packages/pydevd_file_utils.py
    # PATHS_FROM_ECLIPSE_TO_PYTHON='''[["path to local source","path to remote source"]]'''
    # export PATHS_FROM_ECLIPSE_TO_PYTHON='''[["/media/xuananh/data/Dropbox/Viosoft/Eclipse_workspace/validium-nsb-backend1","/home/ubuntu/Dropbox/validium-nsb-backend1"]]'''
    p1 = multiprocessing.Process(target=worker, args=())
    p1.start()
    
    var1 = 0
    while var1 < 3:

        
        var1 = var1 + 1
        print var1
    

