from  platin.language.validate import Validate
from directive import Directive

class IsOver40(object):

    def __call__(self, schemas, keyword, value, request):
        if value <= 40:
            raise ValueError('The age should be over 40, we had %d' % (value))
        return value
Validate.register('over-40', IsOver40)

class Client(Directive):
    __schema__ = 'clientover40'

c = Client(
    surname = "Poquelin",
    firstname = "Jean-Baptiste",
    gender = "male",
    age = 42
)
print c

c = Client(
    surname = "Poquelin",
    firstname = "Jean-Baptiste",
    gender = "male",
    age = 12
)
print c
