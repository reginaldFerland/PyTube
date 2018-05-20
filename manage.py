#! venv/bin/python3

from PyTube import app, db

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

def run(debug=False):
   app.run(host='0.0.0.0', debug=debug)

if __name__ == "__main__":
   run(debug=True)
