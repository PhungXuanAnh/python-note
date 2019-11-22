import logging
import sys

# DEBUG_LEVELV_NUM = 21
# logging.addLevelName(DEBUG_LEVELV_NUM, "DEBUGV")
#  
# def logger_func(self, message, *args, **kws):
#     if self.isEnabledFor(DEBUG_LEVELV_NUM):
#         self._log(DEBUG_LEVELV_NUM, message, args, **kws) 
#  
# setattr(logging.Logger, "debugv", logger_func)
# 
# 
# def logging_func(msg, *args, **kwargs):
#     """
#     Log a message with severity 'DEBUG' on the root logger.
#     """
#     root = logging.root
#     if len(root.handlers) == 0:
#         logging.basicConfig()
#     root.debugv(msg, *args, **kwargs)
#     
# setattr(sys.modules[logging.__name__], "debugv", logging_func)

def add_logging_level(LOGGING_FUNC_NAME="debugv", LEVEL_NAME='DEBUGV', LEVEL_NUM=25):
    '''
    @LOGGING_FUNC_NAME: string: same as info, debug, error, warning
    @LEVEL_NAME: string : same as INFO, DEBUG, ERROR, WARNING
    @LEVEL_NUM: int: same as CRITICAL = 50
                            FATAL = CRITICAL
                            ERROR = 40
                            WARNING = WARN = 30
                            INFO = 20
                            DEBUG = 10
                            NOTSET = 0
    '''
    logging.addLevelName(LEVEL_NUM, LEVEL_NAME)
    
    def logger_func(self, message, *args, **kws):
        if self.isEnabledFor(LEVEL_NUM):
            self._log(LEVEL_NUM, message, args, **kws) 
     
    setattr(logging.Logger, LOGGING_FUNC_NAME, logger_func)
    
    
    def logging_func(msg, *args, **kwargs):
        root = logging.root
        if len(root.handlers) == 0:
            logging.basicConfig()
        getattr(root, LOGGING_FUNC_NAME)(msg, *args, **kwargs)
        
    setattr(sys.modules[logging.__name__], LOGGING_FUNC_NAME, logging_func)


#========================= test
add_logging_level()

logging.basicConfig(level=logging.INFO)
logger_root = logging.getLogger("")
logger_root.debugv("aaaaaaaa")

logging.info("bbbbbbbbbbb")
logging.debugv("ccccccccc")

logger1 = logging.getLogger('logger1')
logger1.debugv('111111111111111')

