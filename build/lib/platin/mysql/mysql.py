#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import MySQLdb as mydb
from ..core.basic import is_sequence, make_list
from cursor import Cursor
from schema import Schema
from errors import *

class MySQL(object):
    """
    MySQL is a wrapper for the MySQLdb interface. It is created with information about
    the server and database to use, the constructor expects a dictionary with the following
    keywords:
        - host
        - port
        - user
        - password
        - database
    """

    def __init__(self,database):
        self._create_database = False
        if 'create_database' in database:
            self._create_database = database['create_database']
        self._check_columns = True
        if 'check_columns' in database:
            self._check_columns = database['check_columns']
        map = {
            'password': 'passwd',
            'database': 'db',
            'user'    : 'user',
            'port'    : 'port',
            'host'    : 'host',
            'unicode' : 'use_unicode',
            'charset' : 'charset',
            'read_default_file': 'read_default_file'
        }
        arguments = {}
        for k,i in database.items():
            if k in map:
                arguments[map[k]] = i
        db = arguments['db']
        del(arguments['db'])
        if arguments['passwd'] is None:
            del(arguments['passwd'])
        keywords = set(map.values())
        for k in arguments:
            if not k in keywords:
                del(arguments[k])
        self._connection_args = arguments
        self._cache = {}
        self._db_name = db
        self.db = self.openConnection(self._connection_args,self._db_name)
        if 'timezone' in database:
            self.executeSQL("SET time_zone = '%s'" % database['timezone'])
        else:
            # we want UTC really
            self.executeSQL("SET time_zone = '+00:00'")

    #
    # utilities
    #

    def createDatabase(self,name):
        with self.cursor() as cursor:
            cursor.execute('create database if not exists %s' % name)

    def describe(self,table):
        if not table in self._cache:
            with self.cursor() as cursor:
                cursor.execute('describe %s' % table)
                all = cursor.fetchall()
                description = Schema()
                for x in all:
                    description[x[0]] = x[1]
            self._cache[table] = description
        return self._cache[table]

    def tableList(self):
        with self.cursor() as cursor:
            cursor.execute('show tables')
            all = [ x[0] for x in cursor.fetchall() ]
        return all

    def writeData(self,data,sql_action,table_name):
        """
        sql_action in the verb, e.g. insert or replace
        data is a list of dictionaries, each keyword is a column name
        """
        description = self.describe(table_name)
        keys = []
        #data = make_list(data)
        for key in data[0]:
            keys.append(key)
        values = []
        for d in data:
            if self._check_columns:
                if not description.checkColumns(d):
                    raise DBInvalidModel("%s" % d)
            values.append('(%s)' % ','.join([ "'%s'" % x for x in d.values() ]))
        sql = '%s into % s (%s) values %s;' % (sql_action,table_name,','.join(keys),','.join(values))
        with self.cursor() as cursor:
            try:
                cursor.execute(sql)
            except Exception as e:
                print sql
                raise DBWriteError(e)

    def cursor(self):
        return Cursor(self)

    def commit(self):
        with self.cursor() as cursor:
            cursor.execute("COMMIT")

    def begin(self):
        with self.cursor() as cursor:
            cursor.execute("BEGIN")

    def rollback(self):
        with self.cursor() as cursor:
            cursor.execute("ROLLBACK")

    def dropTable(self,table_name):
        with self.cursor() as cursor:
            cursor.execute("DROP TABLE %s" % table_name)

    def dropDatabase(self,db_name):
        with self.cursor() as cursor:
            cursor.execute("DROP DATABASE %s" % db_name)

    def executeSQL(self,sql):
        with self.cursor() as cursor:
            cursor.execute(sql)

    def executeSQLAll(self,sql):
        with self.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def executeSQLOne(self,sql):
        with self.cursor() as cursor:
            cursor.execute(sql)
            entry = cursor.fetchone()
            while entry is not None:
                yield entry
                entry = cursor.fetchone()

    def function(self,table,column,function):
        with self.cursor() as cursor:
            cursor.execute('select %s(%s) from %s' % (function,column,table))
            values = cursor.fetchall()
            if len(values) == 0:
                raise ValueError('no data')
            return values[0][0]

    def count(self,table,column,condition):
        count = 0
        with self.cursor() as cursor:
            cursor.execute('select sql_no_cache count(%s) from %s %s' % (column, table, condition))
            res = cursor.fetchall()
            if len(res) > 0:
                count = res[0]
        return count

    def close(self):
        self.db.close()

    def columns(self,table):
        return self.describe(table).keys()

    def _select(self,table,columns=None,extra_sql=None):
        if columns is None:
            columns = self.columns(table)
        if extra_sql is None:
            sql = "select %s from %s" % (','.join(columns),table)
        else:
            sql = "select %s from %s %s" % (','.join(columns),table,extra_sql)
        return sql, columns

    def select(self,*args,**kwargs):
        sql, columns = self._select(*args,**kwargs)
        all = []
        with self.cursor() as cursor:
            cursor.execute(sql)
            found = cursor.fetchall()
            for row in found:
                result = {}
                for i,column in enumerate(columns):
                    result[column] = row[i]
                all.append(result)
        return all

    def select_one(self,*args,**kwargs):
        sql, columns = self._select(*args,**kwargs)
        with self.cursor() as cursor:
            cursor.execute(sql)
            entry = cursor.fetchone()
            while entry is not None:
                result = {}
                for i,column in enumerate(columns):
                    result[column] = entry[i]
                yield result
                entry = cursor.fetchone()

    def where(self,conditions,operator='and'):
        cond = []
        for column,value in conditions.items():
            cond.append('%s%s' % (column,self.sql_condition(value,'=')))
        return '(' + (' ' + operator + ' ').join(cond) + ')'

    #
    # protected methods
    #

    def openConnection(self,args,name):
        """
        Creates a connection with the MySQL server
        """
        db = mydb.connect(**args) 
        cursor = db.cursor()
        cursor.execute('show databases')
        all = set([ x[0] for x in cursor.fetchall() ])
        if not name in all:
            if self._create_database:
                cursor.execute('create database %s' % name)
            else:
                raise IOError('database %s does not exist' % name)
        cursor.execute('use %s' % name)
        cursor.close()
        db.autocommit(True)
        return db

    def ping(self):
        """
        Calls ping and re-connects if the connection is dead
        """
        try:
            self.db.ping(False)
        except (mydb.OperationalError,mydb.InterfaceError):
            self.db = self.openConnection(self._connection_args,self._db_name)
        return self

    def mySQLCursor(self):
        return self.db.cursor()

    def sql_condition(self,value,operator):
        result = '=%s' % value
        if isinstance(value,basestring): 
            result = '%s"%s"' % (operator,value)
        elif is_sequence(value):
            result = ' in (%s)' % ','.join(value)
        elif isinstance(value,dict):
            raise ValueError('Cannot translate a dictionary to SQL')
        else:
            result = '="%s"' % str(value)
        return result
