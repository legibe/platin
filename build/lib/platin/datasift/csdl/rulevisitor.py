from platin.core.config import Config

class RuleVisitor(object):

    def __init__(self,dm,cache = True):
        self._cache = {}
        self._docache = cache
        self._dm = dm
        self._total = 0
        self._missing = 0

    def getSubrules(self,data):
        subrules = set()
        for main_key, entry in data.items():
            for target, rules in entry.items():
                if target == 'rule':
                    for k in rules:
                        subrules.add(k)
        return subrules

    def visitRule(self,stream,visitor,level = 0):
        csdl = None
        if not stream in self._cache:
            try:
                csdl = self._dm.filterInfo(stream)
            except IndexError:
                self._missing += 1
            else:
                if self._docache:
                    self._cache[stream] = csdl
        else:
            csdl = self._cache[stream]
        if csdl is not None:
            deep = visitor(stream,csdl,level)
            self._total += 1

            if deep:
                subrules = self.getSubrules(csdl['target_counts'])
                for subrule in subrules:
                    self.visitRule(subrule,visitor,level + 1)

    def getTotalMissing(self):
        return self._total,self._missing
