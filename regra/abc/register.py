
class Register():
    """Kepping track of subclasses
    """
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__module__+'.'+cls.__qualname__
        if name in cls.subclasses:
            message = "Cannot register module %s as %s; name already in use" % (
                cls.__module__, cls.__module__)
            raise Exception(message)
        cls.subclasses[name] = cls