#! /var/www/html/PyTube/venv/bin/python3
activate_this = '/var/www/html/PyTube/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/html/PyTube')

from PyTube import app as application
