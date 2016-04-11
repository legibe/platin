import ecflow
from ..core.basic import make_list

class PlatinFlow(object):

    def __init__(self,delegate):
        self._delegate = delegate

    def __getattr__(self,attr):
        def wrapper(*args,**kwargs):
            return PlatinFlow(getattr(self._delegate,attr)(*args,**kwargs))

        if attr in set(['add_family','add_task']):
            return wrapper
        return getattr(self._delegate,attr)

    def add_days_of_week(self,days):
        days = make_list(days)
        days = ', '.join(days)
        self.add_variable('DAY_OF_WEEK',days)
        self.add_label('weekday',days)

    def add_days_of_month(self,days):
        days = make_list(days)
        days = [ '%02d' % int(x) for x in days ]
        days = ', '.join(days)
        self.add_variable('DAY_OF_MONTH',days)
        self.add_label('day',days)

    def add_email_status_task(self):
        email = self._delegate.add_task('email')
        email.add_label('recipients','none')
        email.add_defstatus(ecflow.DState.complete)

    def def_status_complete(self):
        self._delegate.add_defstatus(ecflow.DState.complete)

    def __enter__(self,*args,**kwargs):
        return self._delegate.__enter__(*args,**kwargs)

    def __exit__(self,*args,**kwargs):
        return self._delegate.__exit__(*args,**kwargs)
