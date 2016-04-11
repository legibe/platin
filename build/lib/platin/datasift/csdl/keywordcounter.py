
class KeywordCounter(object):

    keywords = {
        'PT_IN':                            'in',
        'PT_STRING_CONTAINS_ANY':           'in',
        'PT_STRING_CONTAINS_ALL':           'in',
        'PT_STRING_CONTAINS_ANY_PHRASE':    'in',
        'PT_STRING_CONTAINS_ALL_PHRASE':    'in',
        'PT_STRING_URL_IN':                 'in',
        'PT_DB_IN':                         'in',
        'PT_DB_ANY':                        'in',
        'PT_STRING_MATCHES_ANY':            'in',
        'PT_STRING_MATCHES_ANY_PHRASE':     'in'
    }

    """
    expects structure of this kind:
    {
        'twitter': {
            operator: count
        },
        'interaction': {
            operator: count
        }
    }
    """
    @classmethod
    def count(self,meta):
        total = 0
        for source, operators in meta.items():
            for operator, count in operators.items():
                if operator in self.keywords:
                    total += count
        return total
