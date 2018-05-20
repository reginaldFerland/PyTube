#! venv/bin/python3

from PyTube import app, db
import unittest
import argparse

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

def run(debug=False):
   app.run(host='0.0.0.0', debug=debug)

def test(verbosity):
    loader = unittest.TestLoader()
    start_dir = './tests/'
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manages PyTube')

    parser.add_argument('--debug', '-d', action='store_true', default=False)
    parser.add_argument('--test', '-t', action='store_true', default=False)
    parser.add_argument('--verbosity', nargs='?', const=2, type=int, default=2, choices=[0,1,2])
    args = parser.parse_args()
    
    # Handle Args
    if(args.test):
        test(args.verbosity)
    else:
        run(debug=args.debug)
