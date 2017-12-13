'''
Format of logging
Attribute name      Format                    Description
args               You shouldn't need to format this yourself.The tuple of arguments merged into msg to produce message, or a dict whose values are used for the merge (when there is only one argument, and it is a dictionary).
asctime            %(asctime)s    Human-readable time when the LogRecord was created. By default this is of the form '2003-07-08 16:49:45,896' (the numbers after the comma are millisecond portion of the time).
created            %(created)f    Time when the LogRecord was created (as returned by time.time()).
exc_info           You shouldn't need to format this yourself.Exception tuple (sys.exc_info) or, if no exception has occurred, None.
filename           %(filename)s    Filename portion of pathname.
funcName           %(funcName)s    Name of function containing the logging call.
levelname          %(levelname)s    Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
levelno            %(levelno)s    Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
lineno             %(lineno)d    Source line number where the logging call was issued (if available).
module             %(module)s    Module (name portion of filename).
msecs              %(msecs)d    Millisecond portion of the time when the LogRecord was created.
message            %(message)s    The logged message, computed as msg % args. This is set when Formatter.format() is invoked.
msg                You shouldn't need to format this yourself.The format string passed in the original logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary objects as messages).
name               %(name)s    Name of the logger used to log the call.
pathname           %(pathname)s    Full pathname of the source file where the logging call was issued (if available).
process            %(process)d    Process ID (if available).
processName        %(processName)s    Process name (if available).
relativeCreated    %(relativeCreated)d    Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
thread             %(thread)d    Thread ID (if available).
threadName         %(threadName)s    Thread name (if available).
'''
import logging, sys

#  configure logging first time 
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S", 
    stream=sys.stdout,
#     filename="/media/xuananh/data/Temp/example.log",
    )


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(pathname)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S", 
    stream=sys.stdout,
    )

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logsfile12.out',
                    filemode='w')

logging.debug('aaaaaaaaaaaaa 1')
logging.info('We processed %d records\n', len("abc")) 

# list all logger
print logging.Logger.manager.loggerDict

# Its effect is to disable all logging calls of severity lvl and below, 
# so that if you call it with a value of INFO, then all INFO and DEBUG 
# events would be discarded, whereas those of severity WARNING and above 
# would be processed according to the logger’s effective level.
logging.disable(logging.INFO)
# To undo it later, you can call:
logging.disable(logging.NOTSET)

#  remove old configure
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
#  re-configure logging 
logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M:%S')  

logging.debug('aaaaaaaaaaaaa 2')
logging.info('We processed %d records\n', len("abc"))


# logging.basicConfig(filename, filemode, format, datefmt, level, stream)  



