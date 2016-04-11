#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import unittest
from mysql import *

class MySQL_test(unittest.TestCase):

    db = None

    def setUp(self):
        self.db = MySQL(dict(
            user = 'root',
            password = 'tooty',
            port = 3306,
            host = 'localhost',
            database = 'test_db'
        ))
        sql = """
        create table if not exists myTable (
            id char(32) not null,
            type char(32) not null,
            unique key(id)
        ) engine=InnoDB;
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            tables = self.db.tableList()
            self.assertEqual(tables,['myTable'])
        data = [
            dict(id=1,type='one'),
            dict(id=2,type='two'),
            dict(id=3,type='three'),
        ]
        sql = self.db.writeData('insert','myTable',data)
        self.db.commit()

    def tearDown(self):
        self.db.dropTable('mytable')
        self.db.dropDatabase('test_db')
        pass

    def test_describe(self):
        self.assertNotEqual(len(self.db.describe('myTable')),0)

    def test_write_fail1(self):
        # fails because id is a unique key
        data = [dict(id=1,type='one')]
        with self.assertRaises(DBWriteError):
            sql = self.db.writeData('insert','myTable',data)

    def test_write_fail2(self):
        # fails the model sent does not match the table schema
        data = [dict(id=1,thetype='one')]
        with self.assertRaises(DBInvalidModel):
            sql = self.db.writeData('insert','myTable',data)
            
    def test_write_succeed1(self):
        # fails because id is a unique key
        data = [dict(id=1,type='one')]
        sql = self.db.writeData('replace','myTable',data)
        self.db.commit()

    def test_write_succeed2(self):
        # same as test_write_fail2 but turn off schema checking
        data = [dict(id=1,type='one')]
        sql = self.db.writeData('replace','myTable',data,check_fields=False)
        self.db.commit()

    def test_rollback(self):
        data = [dict(id=12,type='twelve')]
        self.db.begin()
        sql = self.db.writeData('insert','myTable',data)
        self.db.rollback()
        with self.db.cursor() as cursor:
            cursor.execute('select * from myTable where id=12')
            all = cursor.fetchall()
            self.assertEqual(len(all),0)

    def test_commit(self):
        data = [dict(id=13,type='twelve')]
        self.db.begin()
        sql = self.db.writeData('insert','myTable',data)
        self.db.commit()
        with self.db.cursor() as cursor:
            cursor.execute('select * from myTable where id=13')
            all = cursor.fetchall()
            self.assertEqual(len(all),1)

    def test_reconnect(self):
        self.db.close()
        self.assertNotEqual(len(self.db.describe('myTable')),0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MySQL_test)
    unittest.TextTestRunner(verbosity=2).run(suite)