'''
 Execute the next statement with 'n' (next)
 Repeating the last debugging command with ENTER
 Quitting it all with 'q' (quit)
 Printing the value of variables with 'p' (print)
 Turning off the (Pdb) prompt with 'c' (continue)
 Seeing where you are with 'l' (list)
 
 Stepping into subroutines with 's' (step into subroutine or sub function)
 
'''
import pdb
import sys

class ForkedPdb(pdb.Pdb):
    """A Pdb subclass that may be used
    from a forked multiprocessing child
    usage: ForkedPdb().set_trace

    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin
            
            
if __name__ == '__main__':            
    a = "aaa"
    pdb.set_trace()
    b = "bbb"
    c = "ccc"
    final = a + b + c
    print final
  



