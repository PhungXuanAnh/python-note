import logging

# Its effect is to disable all logging calls of severity lvl and below, 
# so that if you call it with a value of INFO, then all INFO and DEBUG 
# events would be discarded, whereas those of severity WARNING and above 
# would be processed according to the logger’s effective level.
logging.disable(logging.INFO)

# To undo it later, you can call:
logging.disable(logging.NOTSET)