import os
from platin.language.language import Language

class Directive(dict):

    def __init__(self,*args,**kwargs):
        self._schema_path = os.path.join(os.path.dirname(__file__),'schema')
        super(Directive,self).__init__(*args,**kwargs)
        self._schema = self.__class__.__name__.lower()
        if hasattr(self,'__schema__'):
            self._schema = self.__schema__
        self.validate()

    def validate(self):
        l = Language(self._schema,self._schema_path)
        for k,i in self.items():
            if isinstance(i,Directive):
                i.validate()
        new = l.validate(self)
        self.clear()
        self.update(new)

    def __cleanstr__(self,data,level):
        contents = []
        tab = ' ' * (level * 4)
        keys = sorted(data.keys())
        for k in keys: 
            key = str(k)
            key = tab + key + ':' + ' ' * (14 - len(k)) + ' '
            if k[-1] == '_':
                value = '<blob>'
            else:
                i = data[k]
                if isinstance(i,dict):
                    key += '\n'
                    value = self.__cleanstr__(i,level+1)
                elif isinstance(i,list):
                    key += '\n'
                    rows = []
                    for x in i:
                        if isinstance(x,dict):
                            rows.append(self.__cleanstr__(x,level+1))
                        else:
                            rows.append(' ' * (len(key)-len(tab)) + str(x))
                    value = '\n'.join(rows)
                else:
                    value = str(i)
            contents.append('%s%s' % (key,value))
        return '\n'.join(contents)

    
    def __str__(self):
        return self._schema + '\n' + self.__cleanstr__(self,1)
