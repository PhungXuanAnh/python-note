'''
    This module provides utilities to get the absolute filenames so that we can be sure that:
        - The case of a file will match the actual file in the filesystem (otherwise breakpoints won't be hit).
        - Providing means for the user to make path conversions when doing a remote debugging session in
          one machine and debugging in another.

    To do that, the PATHS_FROM_ECLIPSE_TO_PYTHON constant must be filled with the appropriate paths.

    @note:
        in this context, the server is where your python process is running
        and the client is where eclipse is running.

    E.g.:
        If the server (your python process) has the structure
            /user/projects/my_project/src/package/module1.py

        and the client has:
            c:\my_project\src\package\module1.py

        the PATHS_FROM_ECLIPSE_TO_PYTHON would have to be:
            PATHS_FROM_ECLIPSE_TO_PYTHON = [(r'c:\my_project\src', r'/user/projects/my_project/src')]

        alternatively, this can be set with an environment variable from the command line:
           set PATHS_FROM_ECLIPSE_TO_PYTHON=[['c:\my_project\src','/user/projects/my_project/src']]

    @note: DEBUG_CLIENT_SERVER_TRANSLATION can be set to True to debug the result of those translations

    @note: the case of the paths is important! Note that this can be tricky to get right when one machine
    uses a case-independent filesystem and the other uses a case-dependent filesystem (if the system being
    debugged is case-independent, 'normcase()' should be used on the paths defined in PATHS_FROM_ECLIPSE_TO_PYTHON).

    @note: all the paths with breakpoints must be translated (otherwise they won't be found in the server)

    @note: to enable remote debugging in the target machine (pydev extensions in the eclipse installation)
        import pydevd;pydevd.settrace(host, stdoutToServer, stderrToServer, port, suspend)

        see parameter docs on pydevd.py

    @note: for doing a remote debugging session, all the pydevd_ files must be on the server accessible
        through the PYTHONPATH (and the PATHS_FROM_ECLIPSE_TO_PYTHON only needs to be set on the target
        machine for the paths that'll actually have breakpoints).
'''
if __name__ == '__main__':
    '''
    run on remote server: pip install pydevd
    '''
    PATHS_FROM_ECLIPSE_TO_PYTHON=[['/home/xuananh/Dropbox/Viosoft/Eclipse_workspace/Note/debug_sample/pydevd_sample','/home/ubuntu']]
    var1 = 0
    while var1 < 10:
        import pydevd;pydevd.settrace(host="10.76.241.54",
                                      port=5678,
                                      stdoutToServer=True,
                                      stderrToServer=True,)
        var1 = var1 + 1
        print var1
