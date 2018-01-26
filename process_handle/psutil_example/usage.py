import psutil
# pid = 11901
# p = psutil.Process(pid)
# print p.name()
# print p.cmdline()
# print p.ppid()
# print p.status()
# print p.username()
# print p.parent()
# print p.children()
# print p.terminal()
# print p.terminate()

print('list pid {}'.format(psutil.pids()))
for p in psutil.process_iter():
    if p.name() == 'gateone':
        print p.pid
        print p.cmdline()
#         p.terminate()