#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import re
from platin.core.basicfiles import directoryList
from platin.language.language import Language
from platin.language.schemavalidate import SchemaValidate


class SchemaHelp(object):

    def __init__(self,path,classname=None):
        if classname is None:
            self.helpAll(path)
        else:
            self.helpOne(path,classname,'',set())

    def helpAll(self,path):
        files = directoryList(path,'json')
        files = [ x.split('.')[0] for x in files if x[0] != '_']
        files.sort()
        print 'existing classes:'
        print
        print '\n'.join([ '    ' + x for x in files ])
        print

    def helpOne(self,path,classname,indent,seen):

        def reportKeyword(name,keyword):
            definition = SchemaValidate.item
            keywords = sorted([ x for x in keyword.keys()])
            print indent,'%s:' % name
            if 'help' in keyword:
                print indent,'%2s' % ' ', re.sub('\n','\n'+indent+'  ',keyword['help'])
            if 'default' in keyword:
                keyword['required'] = False
            for k in keywords:
                if definition[k]['show_in_help'] and k != 'schema':
                    print indent,'%6s %s: %s' % (' ',k,str(keyword[k]))
            if 'schema' in keyword:
                print indent,'%6s %s (%s)' % (' ','sub-schema',keyword['schema'])
                self.helpOne(path,keyword['schema'],indent + ' ' * 12,seen)
            print

        language = Language(classname,path)
        schema = language._schema
        if not classname in seen:
            seen.add(classname)
            if indent == '':
                print indent,'--- %s ---' % classname
            if language._help is not None:
                print indent,language._help
            if indent == '':
                print
            keywords = sorted(schema.keys())
            for keyword in keywords:
                reportKeyword(keyword,schema[keyword])

if __name__ == '__main__':
    import sys
    classname = None
    if len(sys.argv) == 2:
        classname = sys.argv[1]
    d = SchemaHelp('tutorial/schema',classname)
