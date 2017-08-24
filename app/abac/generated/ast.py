import abc


class Pickler(object):
    def __init__(*args, **kwargs):
        # We have it for compatibility reasons (all node classes has same
        # init signature)
        pass

    @classmethod
    def get_mangled(cls):
        mangled_names = {}
        for c in cls.mro():
            mangled_names.update(getattr(c, "__mangled__", {}).items())
        return mangled_names

    @classmethod
    def mangle_dict(cls, obj):
        # mangle_map is map form normal name to python mangled one.
        mangle_map = cls.get_mangled()
        for k, v in obj.items():
            if k in mangle_map:
                del obj[k]
                obj[mangle_map[k]] = v

    def __getstate__(self):
        # mangled_names is a map from python name to unmangled one.
        mangled_names = {k: v for v, k in self.get_mangled().items()}
        to_pickle = {}
        for k, v in self.__dict__.items():
            to_pickle[mangled_names.get(k,k)] = v
        return to_pickle


class Entity(abc.ABC,Pickler):
    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)    
    
    @property
    @abc.abstractmethod
    def id_(self):
        pass
    
    __mangled__ = {'id': 'id_'}

class UrlEntity(Entity):
    def __init__(self, path=None, *args, **kwargs):
        super(UrlEntity, self).__init__(*args, **kwargs)
        self.path = path    
    
    __mangled__ = {}

class Subject(Entity):
    def __init__(self, name=None, role=None, *args, **kwargs):
        super(Subject, self).__init__(*args, **kwargs)
        self.name = name
        self.role = role    
    
    @property
    @abc.abstractmethod
    def ip(self):
        pass
    
    __mangled__ = {}

