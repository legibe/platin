#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
class Buffered(object):
    """
    A wrapper buffering data on behalf of another object.
    """

    def __init__(self, guest, write_method, buffer_size=2000):
        setattr(self, write_method, self._mywrite_)
        self._guest_write = getattr(guest, write_method)
        self._buffer_size = buffer_size
        self._guest = guest
        self._buffer = [0] * buffer_size
        self._index = 0

    def _mywrite_(self, data, *args, **kwargs):
        for d in data:
            self._buffer[self._index] = d
            self._index += 1
            if self._index == self._buffer_size:
                self.flush(*args, **kwargs)

    def flush(self, *args, **kwargs):
        self._guest_write(self._buffer[:self._index], *args, **kwargs)
        self._index = 0

    def __getattr__(self, attr):
        return getattr(self._guest, attr)
