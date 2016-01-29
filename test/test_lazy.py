# encoding: utf-8

from unittest import TestCase

from marrow.package.lazy import lazy # , lazyload


class MockObject(object):
	calls = 0
	
	@lazy
	def twentyseven(self):
		self.calls = self.calls + 1
		return 27


class TestLazy(TestCase):
	def test_new_contains_no_value(self):
		obj = MockObject()
		assert 'twentyseven' not in obj.__dict__
		assert obj.calls == 0
	
	def test_access_returns_value(self):
		obj = MockObject()
		assert obj.twentyseven == 27
		assert obj.calls == 1
	
	def test_accessed_contains_value(self):
		obj = MockObject()
		obj.twentyseven
		assert 'twentyseven' in obj.__dict__
		assert obj.__dict__['twentyseven'] == 27
		assert obj.calls == 1
	
	def test_multiple_access_calls_once(self):
		obj = MockObject()
		obj.twentyseven
		obj.twentyseven
		assert obj.calls == 1
	
	def test_repr(self):
		assert repr(MockObject.twentyseven.func) in repr(MockObject.twentyseven)
