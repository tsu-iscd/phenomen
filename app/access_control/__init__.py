from abc import abstractclassmethod


class IAccessController:
    @abstractclassmethod
    def is_allowed(self, request, username) -> bool:
        pass