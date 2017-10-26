from flask import Flask

# Create application using provided config
from app.config import DebugConfig as Config
from app.access_control import rbac
from app.access_control import abac

app = Flask(__name__)
app.config.from_object(Config)


ABAC_CONFIG = """
     {
        "entities": [
            {"type": "Subject", "name": "guest", "role": "guest"},
            {"type": "Subject", "name": "user", "role": "user"},
            {"type": "Subject", "name": "admin", "role": "admin"},
            {"type": "UrlEntity", "path":"/"},
            {"type": "UrlEntity", "path": "/motd"},
            {"type": "UrlEntity", "path": "/admin"},
            {"type": "UrlEntity", "path": "/stats"}
        ]
    }
"""

guest_role = rbac.Role(
    name="guest",
    permissions=[
        rbac.Permission("/", rbac.Operation.GET),
    ]
)

admin_role = rbac.Role(
    name="admin",
    permissions=[
        rbac.Permission("/admin", rbac.Operation.GET),
        rbac.Permission("/admin", rbac.Operation.POST),
        rbac.Permission("/admin", rbac.Operation.PUT),
        rbac.Permission("/admin", rbac.Operation.DELETE),
        rbac.Permission("/motd", rbac.Operation.GET),
        rbac.Permission("/motd", rbac.Operation.POST),
        rbac.Permission("/motd", rbac.Operation.PUT),
        rbac.Permission("/motd", rbac.Operation.DELETE),
    ]
)

RBAC_CONFIG = [
    rbac.User("admin", [admin_role, guest_role]),
    rbac.User("guest", [guest_role])
]

#app.access_controller = abac.ABAC(ABAC_CONFIG)
app.access_controller = rbac.RBAC(RBAC_CONFIG)

# Get the routes back (probably not a best way but it works)
from app.views import app