import logging
import sys
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logsfile11.out',
                    filemode='a')
# Until here logs only to file: 'logs_file.out'

# define a new Handler to log to console as well
console = logging.StreamHandler(sys.stdout)

# optional, set the logging level
console.setLevel(logging.INFO)

# set a format which is the same for console use
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Now, we can log to both ti file and console
logging.info('Jackdaws love my big sphinx of quartz.')
logging.info('Hello world')
