import logging

DEBUG_LEVELV_NUM = 21
logging.addLevelName(DEBUG_LEVELV_NUM, "DEBUGV")

def debugv(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_LEVELV_NUM):
        self._log(DEBUG_LEVELV_NUM, message, args, **kws) 

logging.Logger.debugv = debugv


#========================= test
logging.basicConfig(level=logging.INFO)

logger1 = logging.getLogger("")
logger1.debugv("aaaaaaaa")

logging.info("bbbbbbbbbbb")
# logging.debugv("ccccccccc") # Error
