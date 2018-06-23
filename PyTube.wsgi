activate_this = '/home/ubuntu/PyTube/venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from PyTube import app as application
