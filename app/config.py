import os
import uuid

BASEDIR = os.path.abspath(os.path.dirname(__file__))
GENERATED_DIR = os.path.join(BASEDIR, "abac", "generated")

PORT = 9090
REDIS_PORT = 6379

class DebugConfig(object):
    SECRET_KEY = 'debug'
    DEBUG = True


class ProductionConfig(DebugConfig):
    SECRET_KEY = os.getenv('SECRET_KEY', str(uuid.uuid4()))
    DEBUG = False
