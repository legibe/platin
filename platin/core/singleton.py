
class MetaSingleton(type):

    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(MetaSingleton, cls).__call__(*args, **kw)
        return cls.instance


class Singleton(object):
    __metaclass__ = MetaSingleton
