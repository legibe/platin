from collections import Counter
from ...core.tokeniser import Tokeniser

class CSDLCounter(object):

    def __call__(self,csdl,operators):
        counter = Counter()
        tokeniser = Tokeniser('simple')
        words = tokeniser.tokenise(csdl)
        for word in words:
            if word in operators:
                counter[word] += 1
        return counter


