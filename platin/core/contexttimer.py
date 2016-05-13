import timeit

#--------------------------------------------------------------
# Typical use:
#
# with ContextTimer() as t:
#    time.sleep(0.8)
#    print t.snapshot()
#    time.sleep(1.8)
# print t()
#
# 0.801084041595
# 2.60224699974
#--------------------------------------------------------------


class ContextTimer(object):

    def __init__(self):
        self._elapsed = 0.0

    def __enter__(self):
        self._start = timeit.default_timer()
        return self

    def __exit__(self,type, value, traceback):
        self._elapsed = timeit.default_timer() - self._start
        return False

    def __str__(self,format='%1.2f'):
        return format % self._elapsed

    def __call__(self):
        return self._elapsed

    def snapshot(self):
        return timeit.default_timer() - self._start
