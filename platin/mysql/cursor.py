#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------

class Cursor(object):
    """
    Cursor is 
    - a context manager which makes ping the current connection
      to the server and re-connect is necessary
    - a delegator which calls the actual MySQL cursor methods
    """

    def __init__(self,db):
        self._db = db
        self._cursor = None

    def __enter__(self):
        # on entering the context we ping the database, this reconnects 
        # if needed and requests a cursor
        self._db.ping()
        self._cursor = self._db.mySQLCursor()
        return self

    def __exit__(self,type, value, traceback):
        # on leaving the context we close the cursor
        self._cursor.close()
        self._cursor = None
        return False

    def __getattr__(self,attribute):
        # automatic delegation to the MySQL cursor
        if self._cursor is not None:
            return getattr(self._cursor,attribute)
        raise AttributeError('attribute "%s" does not exist' % attribute)
