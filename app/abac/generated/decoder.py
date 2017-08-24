from .ast import *

class ASTFactory(object):
    def __init__(self, *args, **kwargs):
            
        """
        ASTFactory is class that's able to create AST node classes from
        the dict of its fields.
        
        Factory should be used to create AST nodes python dicts or json strings.
        
        To create AST nodes from JSON serialized data use `self.from_json(json_str)`,
        to init from  python dicts, use `self.create(obj)` method.
        
        Both methods look for appropriate construction method and returns its result.
        Each AST node has its own construction method `.create{NodeName}(self, obj)`.
        N.B: Construction methods for abstract classes should be overridden by the user!
        """
    
    def from_json(self, json_str):    
        import json
        return json.loads(json_str, object_hook=self.create)
    
    def create(self, obj):    
        obj_type = obj.get("type","")
        if len(obj_type) == 6:    
            if obj_type == "Entity":    
                Entity.mangle_dict(obj)
                return self.createEntity(obj)
        if len(obj_type) == 9:    
            if obj_type == "UrlEntity":    
                UrlEntity.mangle_dict(obj)
                return self.createUrlEntity(obj)
        if len(obj_type) == 7:    
            if obj_type == "Subject":    
                Subject.mangle_dict(obj)
                return self.createSubject(obj)
    
    def createEntity(self, obj):    
        return Entity(**obj)
    
    def createUrlEntity(self, obj):    
        return UrlEntity(**obj)
    
    def createSubject(self, obj):    
        return Subject(**obj)
    

