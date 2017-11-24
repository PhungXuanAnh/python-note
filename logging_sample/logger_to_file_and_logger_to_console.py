import logging
import sys
#==============================================================
# ket qua la logger 'myapp' va 'root' se in ra stdout theo dinh dang cua logging.basicConfig
# con chi co logger 'myapp' ghi noi dung vao file theo dinh dang cua formtter
#==============================================================

#==============================================================
# create logging named 'root' for log to console
#==============================================================
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)-10s %(name)-8s : [%(pathname)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%d/%m/%y - %H:%M:%S", 
    stream=sys.stdout,
    )
logging.debug('aaaaaaaaaaaaa 1')
logging.info('We processed %d records\n', len("abc")) 

#==============================================================
# create logger1 named 'myapp' for log to file
#==============================================================
logger1 = logging.getLogger('myapp')

hdlr = logging.FileHandler('/tmp/myapp.log')
formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)-10s %(message)s',
                              datefmt="%d/%m/%y - %H:%M:%S")
hdlr.setFormatter(formatter)

logger1.addHandler(hdlr) 
logger1.setLevel(logging.DEBUG)

logger1.error('We have a problem')
logger1.info('While this is just chatty')

#==============================================================
# run logging again
#==============================================================
logging.debug('aaaaaaaaaaaaa 2')
logging.info('We processed %d records\n', len("abcabc")) 