#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from ..core.factory import createFactory
from ..core.basic import to_list
from ..core.basic import timeInSeconds, dateStringInSeconds

ValidationFactory = createFactory('Validation')


class Validate(ValidationFactory):
    pass


class ValidateSetChoice(object):
    def __init__(self, *args):
        self._values = set(args)

    def __call__(self, schemas, keyword, value, request):
        values = to_list(value)
        for v in values:
            if not v in self._values:
                raise IndexError('For keyword "%s", value "%s" is not valid, available choices: %s' % (
                    keyword, v, ', '.join(self._values)))
        return value


class ValidateExclude(object):
    def __init__(self, *args):
        self._values = list(args)

    def __call__(self, schemas, keyword, value, request):
        count = 0
        keywords = self._values + [keyword]
        for value in keywords:
            if value in request and request[value] is not None:
                count += 1
        if count != 1:
            raise ValueError('Keywords %s are exclusive, at least one and only one of them should be defined' % (
                ', '.join(keywords)))
        for k in keywords:
            if k in request and request[k] is None:
                del (request[k])
        return value


class MinumumTime(object):
    def __init__(self, *args):
        self._min = timeInSeconds(args[0])

    def __call__(self, schemas, keyword, value, request):
        value = timeInSeconds(value)
        if value < self._min:
            raise ValueError('The keyword "%s" (%s) should be at least %d seconds' % (keyword, value, self._min))
        return value


class TimeWithUnit(object):
    def __call__(self, schemas, keyword, value, request):
        return timeInSeconds(value)


class DateWithSeconds(object):
    def __call__(self, schemas, keyword, value, request):
        return dateStringInSeconds(value)


class FromFactory(object):
    def __init__(self, *args):
        self._values = args

    def __call__(self, schemas, keyword, value, request):
        for schema in schemas:
            name = '%sFactory' % schema.capitalize()
            if hasattr(factory, name) and value in getattr(factory, name).registered():
                return value
        raise IndexError('Unknown "%s = %s" for schema(s): %s' % (keyword, value, ', '.join(schemas)))


Validate.register('set-choices', ValidateSetChoice)
Validate.register('validate-exclude', ValidateExclude)
Validate.register('minimum-time', MinumumTime)
Validate.register('from-factory', FromFactory)
Validate.register('time-with-unit', TimeWithUnit)
Validate.register('date-with-seconds', DateWithSeconds)

