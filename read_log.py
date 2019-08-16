#!/usr/bin/env python

"""
Real-time log files watcher supporting log rotation.
Works with Python >= 2.6 and >= 3.2, on both POSIX and Windows.

Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT
"""

import os
import time
import errno
import stat
import sys
import re
import argparse
from termcolor import colored


class LogWatcher(object):
    """Looks for changes in all files of a directory.
    This is useful for watching log file changes in real-time.
    It also supports files rotation.

    Example:

    >>> def callback(filename, lines):
    ...     print(filename, lines)
    ...
    >>> lw = LogWatcher("/var/log/", callback)
    >>> lw.loop()
    """

    def __init__(self, folder, callback, extensions=["log"], tail_lines=0,
                 sizehint=1048576):
        """Arguments:

        (str) @folder:
            the folder to watch

        (callable) @callback:
            a function which is called every time one of the file being
            watched is updated;
            this is called with "filename" and "lines" arguments.

        (list) @extensions:
            only watch files with these extensions

        (int) @tail_lines:
            read last N lines from files being watched before starting

        (int) @sizehint: passed to file.readlines(), represents an
            approximation of the maximum number of bytes to read from
            a file on every ieration (as opposed to load the entire
            file in memory until EOF is reached). Defaults to 1MB.
        """
        self.folder = os.path.realpath(folder)
        self.extensions = extensions
        self._files_map = {}
        self._callback = callback
        self._sizehint = sizehint
        assert os.path.isdir(self.folder), self.folder
        assert callable(callback), repr(callback)
        self.update_files()
        for id, file in self._files_map.items():
            file.seek(os.path.getsize(file.name))  # EOF
            if tail_lines:
                try:
                    lines = self.tail(file.name, tail_lines)
                except IOError as err:
                    if err.errno != errno.ENOENT:
                        raise
                else:
                    if lines:
                        self._callback(file.name, lines)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()

    def loop(self, interval=0.1, blocking=True):
        """Start a busy loop checking for file changes every *interval*
        seconds. If *blocking* is False make one loop then return.
        """
        # May be overridden in order to use pyinotify lib and block
        # until the directory being watched is updated.
        # Note that directly calling readlines() as we do is faster
        # than first checking file's last modification times.
        while True:
            self.update_files()
            for fid, file in list(self._files_map.items()):
                self.readlines(file)
            if not blocking:
                return
            time.sleep(interval)

    def log(self, line):
        """Log when a file is un/watched"""
        print(line)

    def listdir(self):
        """List directory and filter files by extension.
        You may want to override this to add extra logic or globbing
        support.
        """
        ls = os.listdir(self.folder)
        if self.extensions:
            return [x for x in ls if os.path.splitext(x)[1][1:]
                    in self.extensions]
        else:
            return ls

    @classmethod
    def open(cls, file):
        """Wrapper around open().
        By default files are opened in binary mode and readlines()
        will return bytes on both Python 2 and 3.
        This means callback() will deal with a list of bytes.
        Can be overridden in order to deal with unicode strings
        instead, like this:

          import codecs, locale
          return codecs.open(file, 'r', encoding=locale.getpreferredencoding(),
                             errors='ignore')
        """
        return open(file, 'rb')

    @classmethod
    def tail(cls, fname, window):
        """Read last N lines from file fname."""
        if window <= 0:
            raise ValueError('invalid window value %r' % window)
        with cls.open(fname) as f:
            BUFSIZ = 1024
            # True if open() was overridden and file was opened in text
            # mode. In that case readlines() will return unicode strings
            # instead of bytes.
            encoded = getattr(f, 'encoding', False)
            CR = '\n' if encoded else b'\n'
            data = '' if encoded else b''
            f.seek(0, os.SEEK_END)
            fsize = f.tell()
            block = -1
            exit = False
            while not exit:
                step = (block * BUFSIZ)
                if abs(step) >= fsize:
                    f.seek(0)
                    newdata = f.read(BUFSIZ - (abs(step) - fsize))
                    exit = True
                else:
                    f.seek(step, os.SEEK_END)
                    newdata = f.read(BUFSIZ)
                data = newdata + data
                if data.count(CR) >= window:
                    break
                else:
                    block -= 1
            return data.splitlines()[-window:]

    def update_files(self):
        ls = []
        for name in self.listdir():
            absname = os.path.realpath(os.path.join(self.folder, name))
            try:
                st = os.stat(absname)
            except EnvironmentError as err:
                if err.errno != errno.ENOENT:
                    raise
            else:
                if not stat.S_ISREG(st.st_mode):
                    continue
                fid = self.get_file_id(st)
                ls.append((fid, absname))

        # check existent files
        for fid, file in list(self._files_map.items()):
            try:
                st = os.stat(file.name)
            except EnvironmentError as err:
                if err.errno == errno.ENOENT:
                    self.unwatch(file, fid)
                else:
                    raise
            else:
                if fid != self.get_file_id(st):
                    # same name but different file (rotation); reload it.
                    self.unwatch(file, fid)
                    self.watch(file.name)

        # add new ones
        for fid, fname in ls:
            if fid not in self._files_map:
                self.watch(fname)

    def readlines(self, file):
        """Read file lines since last access until EOF is reached and
        invoke callback.
        """
        while True:
            lines = file.readlines(self._sizehint)
            if not lines:
                break
            self._callback(file.name, lines)

    def watch(self, fname):
        try:
            file = self.open(fname)
            fid = self.get_file_id(os.stat(fname))
        except EnvironmentError as err:
            if err.errno != errno.ENOENT:
                raise
        else:
            self.log("watching logfile %s" % fname)
            self._files_map[fid] = file

    def unwatch(self, file, fid):
        # File no longer exists. If it has been renamed try to read it
        # for the last time in case we're dealing with a rotating log
        # file.
        self.log("un-watching logfile %s" % file.name)
        del self._files_map[fid]
        with file:
            lines = self.readlines(file)
            if lines:
                self._callback(file.name, lines)

    @staticmethod
    def get_file_id(st):
        if os.name == 'posix':
            return "%xg%x" % (st.st_dev, st.st_ino)
        else:
            return "%f" % st.st_ctime

    def close(self):
        for id, file in self._files_map.items():
            file.close()
        self._files_map.clear()


# ===================================================================
# --- tests
# ===================================================================

def test():
    import unittest
    import atexit

    TESTFN = '$testfile.log'
    TESTFN2 = '$testfile2.log'
    PY3 = sys.version_info[0] == 3

    if PY3:
        def b(s):
            return s.encode("latin-1")
    else:
        def b(s):
            return s

    class TestLogWatcher(unittest.TestCase):

        def setUp(self):
            def callback(filename, lines):
                self.filename.append(filename)
                for line in lines:
                    self.lines.append(line)

            self.filename = []
            self.lines = []
            self.file = open(TESTFN, 'w')
            self.watcher = LogWatcher(os.getcwd(), callback)

        def tearDown(self):
            self.watcher.close()
            self.remove_test_files()

        def write_file(self, data):
            self.file.write(data)
            self.file.flush()

        @staticmethod
        @atexit.register
        def remove_test_files():
            for x in [TESTFN, TESTFN2]:
                try:
                    os.remove(x)
                except EnvironmentError:
                    pass

        def test_no_lines(self):
            self.watcher.loop(blocking=False)

        def test_one_line(self):
            self.write_file('foo')
            self.watcher.loop(blocking=False)
            self.assertEqual(self.lines, [b"foo"])
            self.assertEqual(self.filename, [os.path.abspath(TESTFN)])

        def test_two_lines(self):
            self.write_file('foo\n')
            self.write_file('bar\n')
            self.watcher.loop(blocking=False)
            self.assertEqual(self.lines, [b"foo\n", b"bar\n"])
            self.assertEqual(self.filename, [os.path.abspath(TESTFN)])

        def test_new_file(self):
            with open(TESTFN2, "w") as f:
                f.write("foo")
            self.watcher.loop(blocking=False)
            self.assertEqual(self.lines, [b"foo"])
            self.assertEqual(self.filename, [os.path.abspath(TESTFN2)])

        def test_file_removed(self):
            self.write_file("foo")
            try:
                os.remove(TESTFN)
            except EnvironmentError:  # necessary on Windows
                pass
            self.watcher.loop(blocking=False)
            self.assertEqual(self.lines, [b"foo"])

        def test_tail(self):
            MAX = 10000
            content = '\n'.join([str(x) for x in range(0, MAX)])
            self.write_file(content)
            # input < BUFSIZ (1 iteration)
            lines = self.watcher.tail(self.file.name, 100)
            self.assertEqual(len(lines), 100)
            self.assertEqual(lines, [b(str(x)) for x in range(MAX - 100, MAX)])
            # input > BUFSIZ (multiple iterations)
            lines = self.watcher.tail(self.file.name, 5000)
            self.assertEqual(len(lines), 5000)
            self.assertEqual(lines, [b(str(x)) for x in range(MAX - 5000, MAX)])
            # input > file's total lines
            lines = self.watcher.tail(self.file.name, MAX + 9999)
            self.assertEqual(len(lines), MAX)
            self.assertEqual(lines, [b(str(x)) for x in range(0, MAX)])
            #
            self.assertRaises(ValueError, self.watcher.tail, self.file.name, 0)
            LogWatcher.tail(self.file.name, 10)

        def test_ctx_manager(self):
            with self.watcher:
                pass

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestLogWatcher))
    unittest.TextTestRunner(verbosity=2).run(test_suite)


def callback(filename, lines):
    for line in lines:
        print(line)


"""
Text colors:
    grey
    red
    green
    yellow
    blue
    magenta
    cyan
    white
Text highlights:
    on_grey
    on_red
    on_green
    on_yellow
    on_blue
    on_magenta
    on_cyan
    on_white
Attributes:
    bold
    dark
    underline
    blink
    reverse
    concealed
"""


def get_level_color(level):
    if level == 'WARNING':
        return 'yellow'
    elif level == 'ERROR ':
        return 'red'
    elif level == 'INFO   ' or level == 'DEBUG  ':
        return 'green'
    else:
        return 'magenta'


def coloured(s, color):
    return '\033[1;%s%s\033[1;m' % (color, s.decode())


def callback_color(filename, lines):
    """
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)1.1s %(asctime)s] %(message)s',)

    WARNING [2019-07-23 02:36:45,411] [connection.start:24] : Connected to redis://redis:6379//
    ERROR   [2019-07-23 02:36:45,421] [mingle.sync:43] : mingle: searching for neighbors
    INFO    [2019-07-23 02:35:51,892] [tasks.run_project:73] : {'node_name': 'scrapy', 'status': 'ok', 'jobid': '96752526acf211e997a70242c0a87003', 'spider': 'facebook'}
    WARNING [2019-07-23 02:36:45,411] [connection.start:24] : Connected to redis://redis:6379//

    """
    RED = "31m"
    BLUE = "34m"
    GREEN = "32m"
    YELLOW = "33m"
    MAGENTA = "35m"

    while lines:
        line = lines.pop(0).rstrip()
        noheader = False
        if line.startswith(b"E") or line.startswith(b"Traceback"):
            color = RED
        elif line.startswith(b"D"):
            color = BLUE
        elif line.startswith(b"I"):
            color = GREEN
        elif line.startswith(b"W"):
            color = YELLOW
        else:
            noheader = True
            color = MAGENTA

        if noheader:
            print(line.decode())
        else:
            end_header = line.find(b'] :')
            if not end_header:
                end_header = line.find(b':')
            header = coloured(line[0:end_header + 1], color)
            line = line[end_header + 1:]
            print(header + line.decode())


def callback_color1(filename, lines):
    """
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)1.1s %(asctime)s] %(message)s',)
    012345678901234567890123456789012345678901234567890123456789
    WARNING [2019-07-23 02:36:45,411] [connection.start:24] : Connected to redis://redis:6379//
    ERROR   [2019-07-23 02:36:45,421] [mingle.sync:43] : mingle: searching for neighbors
    INFO    [2019-07-23 02:35:51,892] [tasks.run_project:73] : {'node_name': 'scrapy', 'status': 'ok', 'jobid': '96752526acf211e997a70242c0a87003', 'spider': 'facebook'}
    WARNING [2019-07-23 02:36:45,411] [connection.start:24] : Connected to redis://redis:6379//

    """
    INFO = 'INFO   '
    ERROR = 'ERROR  '
    WARNING = 'WARNING'
    DEBUG = 'DEBUG  '

    lv_len = 7
    time_len = 33
    
    while lines:
        line = lines.pop(0).rstrip()
        line = line.decode()
        if not line:
            print('')
            continue
        if line[0:lv_len] == INFO:
            level = colored(INFO, 'green')
        elif line[0:lv_len] == WARNING:
            level = colored(WARNING, 'yellow')
        elif line[0:lv_len] == ERROR:
            level = colored(ERROR, 'red')
        elif line[0:lv_len] == DEBUG:
            level = colored(DEBUG, 'green')
        elif line[0:lv_len] == 'Traceback':
            level = colored(line, 'red')
            continue
        else:
            print(line)
            continue

        time = colored(line[lv_len + 1: time_len + 1], 'cyan')

        log_module = re.search(r'(\[[a-z0-9_]+\.[a-z0-9_]+:[0-9]+\] \:)', line[time_len + 1:])
        if log_module:
            log_module = log_module.group(1)
            log_module_len = len(log_module)
            log_module = colored(log_module, 'blue')

        print(level + time + log_module)

        # start_msg = level_len + log_time_len + log_module_len + 9
        # msg = line[start_msg:]

        # numbers = re.findall(r'[0-9]+', msg)
        # numbers = set(numbers)
        # print(numbers)
        # for n in numbers:
        #     msg = msg.replace(n, colored(n, 'red'))

        # header = line[0:start_msg]

        # print(header + msg)


def parse_cmdline():
    parser = argparse.ArgumentParser(
        description="Read log file: read_log.py path_to_file")

    parser.add_argument('-i', '--input',
                        metavar='FILE',
                        dest='input',
                        help='Enter a file path or directory path',
                        required=True,
                        type=str)

    parser.add_argument('-l', '--lines',
                        metavar='NUMBER',
                        dest='lines',
                        help='Enter a number of line to read',
                        type=int)

    parser.add_argument('-c', '--color',
                        metavar='Bool',
                        dest='color',
                        help='Highligh color or not',
                        type=bool)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # LogWatcher.tail('foo.log', 10)

    args = parse_cmdline()
    print(args.input)
    print(args.lines)
    print(args.color)

    if args.color:
        cb = callback_color1
    else:
        cb = callback

    if args.lines:
        watcher = LogWatcher(args.input, cb, tail_lines=args.lines)
    else:
        watcher = LogWatcher(args.input, cb)

    watcher.loop()
