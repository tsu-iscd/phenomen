import enum
from abc import abstractclassmethod
from typing import List


class Operation(enum.Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


class Permission:
    def __init__(self, entity, operation: Operation) -> None:
        self.entity = entity
        self.operation = operation

    def __str__(self):
        return self.entity + ":" + self.operation.value

    def __eq__(self, other):
        return self.entity == other.entity and self.operation.value == other.operation.value


class IRole:
    @abstractclassmethod
    def grant_permission(self, permission: Permission) -> None:
        """
        Grants a role the permission to perform an operation on a entity
        to a set of permissions assigned to a role.
        """
        pass

    @abstractclassmethod
    def revoke_permission(self, permission: Permission) -> None:
        """
        Revokes a role the permission to perform an operation on a entity
        from a set of permissions assigned to a role.
        """
        pass

    @abstractclassmethod
    def has_permission(self, permission: Permission) -> bool:
        """
        Checks if a role has the given permission.
        """
        pass


class IUser:
    @abstractclassmethod
    def get_username(self) -> str:
        """ Returns user's name. """
        pass

    @abstractclassmethod
    def get_roles(self) -> List[IRole]:
        """ Returns user's roles. """
        pass

    @abstractclassmethod
    def add_role(self, role: IRole) -> None:
        """ Assign a role to user. """
        pass

    @abstractclassmethod
    def add_roles(self, roles: List[IRole]) -> None:
        """ Assign roles to user. """
        pass

    @abstractclassmethod
    def delete_role(self, role: IRole) -> None:
        """ Removes the given role. """
        pass


class ISession:
    def __init__(self, user: IUser, roles: List[IRole]):
        self.user = user
        self.roles = roles

    @abstractclassmethod
    def add_active_role(self, role: IRole):
        """
        Adds a role as an active role of a session whose owner is a given user.
        """
        pass

    @abstractclassmethod
    def get_user(self)-> IUser:
        """
        Returns user owned the session.
        """
        pass

    @abstractclassmethod
    def drop_active_role(self, role: IRole):
        """
        Deletes a role from the active role set of a session owned by a given user
        """
        pass


class IRBAC:
    @abstractclassmethod
    def check_access(self, session: ISession, entity, operation: Operation) -> bool:
        """
        This function returns a Boolean value meaning whether the subject of a given session is
        allowed or not to perform a given operation on a given object
        """
        pass
