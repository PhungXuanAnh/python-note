import multiprocessing

def worker():
    var1 = 4
    while var1 < 6:
        import pydevd;pydevd.settrace(host="10.76.241.54",
                                      port=5678,
                                      stdoutToServer=True,
                                      stderrToServer=True,
                                      )
        var1 = var1 + 1
        print var1
    
    
if __name__ == '__main__':
    '''
    run on remote machine and local machine: pip install pydevd
    '''
    # khong duoc thi chay thu dong duoi
    # PATHS_FROM_ECLIPSE_TO_PYTHON='''[["path to local source","path to remote source"]]'''
    # export PATHS_FROM_ECLIPSE_TO_PYTHON='''[["/home/xuananh/Dropbox/Viosoft/Eclipse_workspace/Note","/home/ubuntu/python-note/a"]]'''
    p1 = multiprocessing.Process(target=worker, args=())
    p1.start()
    
    var1 = 0
    while var1 < 3:
#         import pydevd;pydevd.settrace(host="10.76.241.54",
#                                       port=5678,
#                                       stdoutToServer=True,
#                                       stderrToServer=True,
#                                       patch_multiprocessing=True,)
        
        var1 = var1 + 1
        print var1
    

