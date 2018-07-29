# encoding: utf-8

import pytest

from unittest import TestCase

from marrow.package.loader import traverse, load

from test import helper


class Recorder(object):
	def __init__(self, traversal=None):
		self._traversal = traversal or []
	
	def callable(self):
		self._traversal.append('!')
		return self
	
	def __getattr__(self, name):
		if name in ('bogan', 'canary'):
			raise AttributeError()
		
		self._traversal.append('.' + name)
		return self
	
	def __getitem__(self, name):
		if name == 'canary':
			raise KeyError()
		
		self._traversal.append('[' + str(name) + ('i' if isinstance(name, int) else '') + ']')
		return self


class TestTraversal(TestCase):
	def test_empty_traversal_returns_haystack(self):
		assert traverse(Recorder(), '')._traversal == []
	
	def test_simple_attribute_reference(self):
		assert traverse(Recorder(), 'foo')._traversal == ['.foo']
	
	def test_simple_attribute_reference_nested(self):
		assert traverse(Recorder(), 'foo.bar')._traversal == ['.foo', '.bar']
	
	def test_reference_numeric(self):
		assert traverse(Recorder(), '27')._traversal == ['[27i]']
	
	def test_reference_bogan(self):
		assert traverse(Recorder(), 'bogan')._traversal == ['[bogan]']
	
	def test_reference_callable(self):
		assert traverse(Recorder(), 'callable', executable=True)._traversal == ['!']
	
	def test_reference_bad(self):
		with pytest.raises(LookupError):
			assert traverse(Recorder(), 'canary')
	
	def test_reference_default(self):
		assert traverse(Recorder(), 'canary', default=27) == 27


class TestLoader(TestCase):
	def test_invalid_import_nodefault(self):
		with pytest.raises(ImportError):
			assert load('foo.bar:baz')
	
	def test_invalid_import_default(self):
		assert load('foo.bar:baz', default="hi") is "hi"
	
	def test_basic_import(self):
		assert load('test.helper:Example') is helper.Example
	
	def test_basic_entrypoint(self):
		assert load('py.test', 'console_scripts') is pytest.main
	
	def test_unknown_entrypoint(self):
		with pytest.raises(LookupError):
			assert load('bob.dole', 'console_scripts')
