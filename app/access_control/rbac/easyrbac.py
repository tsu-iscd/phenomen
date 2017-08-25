from .interfaces import *
from typing import List
from app.access_control import IAccessController


class User(IUser):
    def __init__(self, username: str, roles: List[IRole]):
        super(User, self).__init__()
        self.username = username
        self.roles = roles

    def get_username(self) -> str:
        return self.username

    def get_roles(self):
        return self.roles

    def add_role(self, role: IRole):
        self.roles.append(role)

    def add_roles(self, roles: List[IRole]):
        self.roles.extend(roles)

    def delete_role(self, role: IRole):
        self.roles.remove(role)


class Role(IRole):
    def __init__(self, name: str, permissions: List[Permission]):
        super(Role, self).__init__()
        self.name = name
        self.permissions = permissions

    def grant_permission(self, permission: Permission):
        self.permissions.append(permission)

    def revoke_permission(self, permission: Permission):
        self.permissions.remove(permission)

    def has_permission(self, permission: Permission):
        for p in self.permissions:
            if p == permission:
                return True
        return False


class Session(ISession):
    def __init__(self, user: IUser, roles: List[IRole]):
        super(Session, self).__init__()
        self.user = user
        self.roles = roles

    def get_user(self):
        return self.user

    def add_active_role(self, role: IRole):
        self.roles.append(role)

    def drop_active_role(self, role: IRole):
        self.roles.remove(role)


class PIP:
    def __init__(self, users: List[IUser]) -> None:
        self.users = users


class PDP(IRBAC):
    def __init__(self) -> None:
        super(PDP, self).__init__()

    def check_access(self, session: ISession, entity, operation: Operation) -> bool:
        user_roles = session.get_user().get_roles()
        checked_permission = Permission(entity, operation)
        for role in user_roles:
            if role.has_permission(checked_permission):
                return True
        return False

    def check_roled_access(self, roles: List[IRole], entity, operation: Operation) -> bool:
        if not roles:
            return False
        checked_permission = Permission(entity, operation)
        for role in roles:
            if role.has_permission(checked_permission):
                return True
        return False


class RBAC(IAccessController):
    def __init__(self, config: List[IUser]) -> None:
        super(RBAC, self).__init__()
        self.pip = PIP(config)
        self.pdp = PDP()

    def is_allowed(self, request, username) -> bool:
        for user in self.pip.users:
            if user.get_username() == username:
                return self.pdp.check_roled_access(user.get_roles(), request.path, Operation(request.method))
        return False
