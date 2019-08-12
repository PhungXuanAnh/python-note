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

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-7s [%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] : %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
#     filename="/media/xuananh/data/Temp/example.log",
    )

logging.debug('aaaaaaaaaaaaa 2')
logging.info('aaaaaaaaaaaaa 2')
logging.error('aaaaaaaaaaaaa 2')
logging.warning('aaaaaaaaaaaaa 2')
