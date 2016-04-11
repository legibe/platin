#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
__all__ = ['DBException','DBInvalidModel','DBUnknownDatabase','DBWriteError']

class DBException(Exception):
    pass 

class DBInvalidModel(DBException):
    pass

class DBExceptionWrapper(DBException):
    def __init__(self,exception):
        super(DBExceptionWrapper,self).__init__('%s - %s' % (exception.__str__(),type(exception)))

class DBUnknownDatabase(DBExceptionWrapper):
    pass

class DBWriteError(DBExceptionWrapper):
    pass

