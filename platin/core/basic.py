#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import re
import os
from collections import OrderedDict, Sequence


def class_of(a):
    return a.__class__


def class_name_of(a):
    return classof(a).__name__


def is_list(a):
    return type(a) == list or type(a) == tuple


def is_sequence(a):
    return isinstance(a, Sequence)


def is_sequence_and_not_string(a):
    return isinstance(a, Sequence) and not isinstance(a, basestring)


def is_dict(a):
    return isinstance(a, dict)


def make_list(a):
    if not is_list(a):
        a = [a]
    return a
to_list = make_list


def no_list(a): 
    if is_list(a):
        a = a[0]
    return a


def find_all_variables(a):
    """
    Find all variables are represented as ${varname} in a string
    """
    return set(re.findall('\${(.*?)}', a))


def substitute_env_variables(a):
    """
    Finds variables in string in the form: ${varname} and replaces
    their value if an environment variable with the same name is found
    """
    if isinstance(a, basestring):
        vars = re.findall('\${(.*?)}', a)
        for var in vars:
            default = var.split(':-')
            v = os.getenv(default[0])
            if v is None and len(default) > 1:
                v = default[1]
            if v is not None:
                a = re.sub('\${%s}' % var, v, a)
    return a


def dict_substitute_env_variables(a):
    for k, i in a.items():
        if isinstance(i, basestring):
            a[k] = substitute_env_variables(i)
    return a


def substitute_from_dict(a, variables):
    """Substitutes variables of the form ${varname} with
    values provided in a dictionary
    """
    if isinstance(a,basestring):
        vars = re.findall('\${(.*?)}', a)
        for var in vars:
            if var in variables:
                a = re.sub('\${%s}' % var,variables[var], a)
    return a


def sortSequence(s):
    """
    Arbitrarily sorts nested sequences
    """
    for i in range(len(s)):
        v = s[i]
        if isinstance(v,dict):
            v = sortDict(v)
        elif isinstance(v,Sequence) and not isinstance(v, basestring):
            v = sortSequence(v)
        s[i] = v
    return s


def sortDict(d):
    """
    Recursively sorts dictionaries which can be nested and stores them
    in Oredered dicts.
    """
    od = OrderedDict()
    for key in sorted(d.keys()):
        if isinstance(d[key], dict):
            od[key] = sortDict(d[key])
        elif isinstance(d[key],Sequence) and not isinstance(d[key], basestring):
            od[key] = sortSequence(d[key])
        else:
            od[key] = d[key]
    return od


def timeInSeconds(s):
    """
    :param s: a string, for example 12, 12mn, 4h, 4hours, 2 days etc...
    :return: the time in seconds
    """
    factors = {
        's': 1,
        'second': 1,
        'seconds': 1,
        'mn': 60,
        'm': 60,
        'minute': 60,
        'minutes': 60,
        'h': 3600,
        'hour': 3600,
        'hours': 3600,
        'd': 86400,
        'day': 86400,
        'days': 86400,
    }

    s = str(s).lower().strip()
    negative = False
    if s[0] == '-':
        negative = True
        s = s[1:]
    unit = re.findall('[a-z]+$', s)
    number = int(re.findall('^[0-9]+', s)[0])
    factor = 1
    if len(unit) > 0:
        if not unit[0] in factors:
            raise ValueError('In time %s, unknow unit: %s' % (s,unit[0]))
        factor = factors[unit[0]]
        if negative:
            factor = -factor
    return number * factor


def roundedDateMask(timeinseconds):
    if timeinseconds >= 3600:
        return '%Y%m%d%H0000'
    elif timeinseconds >= 60:
        return '%Y%m%d%H%M00'
    else:
        return '%Y%m%d%H%M%S'


def dateStringInSeconds(date):
    date = str(date)
    format = 'yyyymmddhhMMss'
    if len(date) < len(format):
        date += '0' * (len(format) - len(date))
    return date

        
def findInDicList(where,keys,value):
    if len(keys) == 0:
        return False
    if keys[0] in where:
        if len(keys) == 1:
            return where[keys[0]] == value
        elif isinstance(where[keys[0]],dict):
            return findInDicList(where[keys[0]],keys[1:],value)
    return False

        
def findInDictDotted(where,path,value):
    keys = path.split('.')
    return findInDicList(where,keys,value)


def bigNumber(value):
    s = str(value)
    l = s.split('.')
    whole = l[0]
    dec = ''
    if len(l) > 1:
        dec = l[1]
    new = ''
    ll = len(whole)
    for i in range(ll):
        indx = ll - i - 1
        new += whole[i]
        if indx % 3 == 0 and indx != 0:
            new += ','
    if len(dec) > 0:
        new += '.' + dec
    return new



def bigNumberShort(value):
    abbreviations = ['', 'K', 'M', 'B']

    value = float(value)
    i = 0
    while value >= 1000 and i < len(abbreviations):
        i += 1
        value /= 1000
    v = str(value)
    v = v.replace('.0', '')
    return v + abbreviations[i]


#----------------------------------------------------------------------------
# merging dictionaries
#----------------------------------------------------------------------------

def mergedicts_overwrite(a, b):
    """
    Merge dictionaries, if a key in a is in b, it is
    overriden with the value in b
    """
    return dict(a,**b)


def mergedicts_keep(a,b):
    """
    Merge dictionaties, if a key in b is in a, it is
    not touched.
    """
    d = dict(a)
    for k,i in b.items():
        if not k in a:
            d[k] = i
    return d

