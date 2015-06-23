__author__ = 'Rainbowfox'
import logging

# import sys

from RetrievalModel.Constants import LOG_DIR

"some constants used here"

log = logging.getLogger('ir')
log.setLevel(logging.INFO)

# ch = logging.StreamHandler(sys.stdout)

ch = logging.FileHandler(LOG_DIR)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(lineno)d  - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
