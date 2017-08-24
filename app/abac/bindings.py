from .generated import ast
from .generated.decoder import ASTFactory

###############################################################################
# Implementation of the abstract classes
###############################################################################
class UrlEntity(ast.UrlEntity):
    @property
    def id_(self):
        return self.path


class Subject(ast.Subject):
    def __init__(self, name=None, request=None, *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)
        self.request = request

    @property
    def id_(self):
        return self.name

    @property
    def ip(self):
       return self.request.remote_addr


class MyFactory(ASTFactory):
    def createUrlEntity(self, obj):
        return UrlEntity(**obj)
    def createSubject(self, obj):
        return Subject(**obj)

###############################################################################