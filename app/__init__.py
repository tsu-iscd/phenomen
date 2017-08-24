from flask import Flask


# Create application using provided config
from app.config import DebugConfig as Config
app = Flask(__name__)
app.config.from_object(Config)


# Initialize access control
from app.abac import AccessController
app.access_controller = AccessController()


# Get the routes back (probably not a best way but it works)
from app.views import app