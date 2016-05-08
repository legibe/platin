import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from core.basic import *


class TestBasicFunctions(unittest.TestCase):

	def test_class_of(self):
		self.assertEqual(self.__class__,class_of(self))

	def test_class_name_of(self):
		self.assertEquals(self.__class__.__name__,class_name_of(self))

	def test_is_list(self):
		self.assertTrue(is_list([12]))
		self.assertTrue(is_list((1,2,3)))
		self.assertFalse(is_list('hello'))
		self.assertFalse(is_list(43.5))

	def test_is_sequence(self):
		self.assertTrue(is_sequence([1,2,3]))
		self.assertTrue(is_sequence((1, 2, 3)))
		self.assertTrue(is_sequence('hello'))
		self.assertFalse(is_sequence({ 1, 2, 3, 4 }))
		self.assertFalse(is_sequence({'a': 1, 'b': 2}))
		self.assertFalse(is_sequence(12))


	def test_is_sequence_and_not_string(self):
		self.assertTrue(is_sequence_and_not_string([1, 2, 3]))
		self.assertTrue(is_sequence_and_not_string((1, 2, 3)))
		self.assertFalse(is_sequence_and_not_string('hello'))
		self.assertFalse(is_sequence_and_not_string({1, 2, 3, 4}))
		self.assertFalse(is_sequence_and_not_string({'a': 1, 'b': 2}))
		self.assertFalse(is_sequence_and_not_string(12))


	def test_timeInSeconds(self):
		self.assertEquals(1, time_in_seconds('1'))
		self.assertEquals(1,  time_in_seconds('1s'))
		self.assertEquals(60, time_in_seconds('1mn'))
		self.assertEquals(60, time_in_seconds('1 mn'))
		self.assertEquals(60, time_in_seconds('  1 mn '))
		self.assertEquals(60, time_in_seconds('  1 minute '))
		self.assertEquals(120, time_in_seconds('2 minutes'))
		self.assertEquals(72000, time_in_seconds('20 hours'))
		self.assertEquals(72000, time_in_seconds('20h'))
		self.assertEquals(172800, time_in_seconds('2 days'))

	def test_big_number(self):
		self.assertEquals('1,000,000', big_number(1000000))
		self.assertEquals('22,345', big_number(22345))
		self.assertEquals('1,000,000,000', big_number(1000000000))

	def test_big_number_short(self):
		self.assertEquals('1M', big_number_short(1000000))
		self.assertEquals('32K', big_number_short(32000))
		self.assertEquals('12B', big_number_short(12000000000))

	def test_merge_dicts_overwrite(self):
		self.assertEquals({'a': 3, 'c': 4, 'b': 2}, merge_dicts_overwrite({'a': 1, 'b': 2}, {'a': 3, 'c': 4}))

	def test_merge_dicts_keep(self):
		self.assertEquals({'a': 1, 'c': 4, 'b': 2}, merge_dicts_keep({'a': 1, 'b': 2}, {'a': 3, 'c': 4}))


if __name__ == '__main__':
	unittest.main()