import sys
from flask_script import Manager
from app import app


if sys.version_info < (3, 6):
        sys.exit("Python < 3.6 is not supported")

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
