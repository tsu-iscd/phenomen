from .interfaces import *
from typing import List
from app.access_control import IAccessController


class User(IUser):
    pass


class Role(IRole):
    pass


class Session(ISession):
    pass


class PIP:
    pass


class PDP(IRBAC):
    pass


class RBAC(IAccessController):
    def __init__(self) -> None:
        super(RBAC, self).__init__()

    def is_allowed(self, request, username) -> bool:
        return True
