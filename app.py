from flask import Flask

app = Flask(__name__)

# if not app.debug:
import logging
logger = logging.getLogger()
logger.handlers = []
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('tmp/logging.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
    
from view import *

if __name__ == '__main__':
    app.run(debug=True)