#! venv/bin/python3

from PyTube import app

def run(debug=False):
   app.run(host='0.0.0.0', debug=debug)

if __name__ == "__main__":
   run(debug=True)
