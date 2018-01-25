import logging
#  remove old configure
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)