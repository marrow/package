import pytest

from unittest import TestCase

from marrow.package.canonical import name

from test import helper


xfail_qualname = pytest.mark.xfail(
		not hasattr(helper.Example, '__qualname__'),
		raises = LookupError,
		reason = "Requires __qualname__ support introduced in Python 3.3."
	)


class TestResolver(TestCase):
	"""This test suite identifies the capabilities of your interpreter.
	
	If a test is skipped/xfails a reason will be given outlining the implication for your own applications.
	"""
	
	@xfail_qualname
	def test__resolve__of_a_closure(self):
		def closure():
			pass
		
		assert name(closure) == 'test.test_canonical:TestResolver.test__resolve__of_a_closure.<locals>.closure'
	
	def test__resolve__of_a_module_level_class(self):
		assert name(helper.Example) == 'test.helper:Example'
	
	def test__resolve__of_a_module_level_class_classmethod(self):
		assert name(helper.Example.classmethod) == 'test.helper:Example.classmethod'
	
	def test__resolve__of_a_module_level_class_instance(self):
		assert name(helper.instance) == 'test.helper:Example'
	
	def test__resolve__of_a_module_level_class_method(self):
		assert name(helper.Example.instance) == 'test.helper:Example.instance'
	
	def test__resolve__of_a_module_level_class_staticmethod(self):
		assert name(helper.Example.staticmethod) == 'test.helper:Example.staticmethod'
	
	def test__resolve__of_a_module_level_function(self):
		assert name(helper.bare) == 'test.helper:bare'
	
	def test__resolve__of_a_module_level_instance_classmethod(self):
		assert name(helper.instance.classmethod) == 'test.helper:Example.classmethod'
	
	def test__resolve__of_a_module_level_instance_method(self):
		assert name(helper.instance.instance) == 'test.helper:Example.instance'
	
	def test__resolve__of_a_module_level_instance_staticmethod(self):
		assert name(helper.instance.staticmethod) == 'test.helper:Example.staticmethod'
	
	@xfail_qualname
	def test__resolve__of_a_nested_class_deep(self):
		assert name(helper.Example.Pandora.Box) == 'test.helper:Example.Pandora.Box'
	
	@xfail_qualname
	def test__resolve__of_a_nested_class_deep_method(self):
		assert name(helper.Example.Pandora.Box.nested) == 'test.helper:Example.Pandora.Box.nested'
	
	def test__resolve__of_a_nested_class_shallow(self):
		assert name(helper.Example.Pandora) == 'test.helper:Example.Pandora'
	
	def test__resolve__of_a_module_level_decorated_function(self):
		assert name(helper.decorated_shallow) == 'test.helper:decorated_shallow'
	
	def test__resolve__of_a_module_level_decorated_decorated_function(self):
		assert name(helper.decorated_deep) == 'test.helper:decorated_deep'
	
	def test__resolve__of_a_module_level_decorated_method(self):
		assert name(helper.Example.decorated_shallow) == 'test.helper:Example.decorated_shallow'
		
	def test__resolve__of_a_module_level_decorated_decorated_method(self):
		assert name(helper.Example.decorated_deep) == 'test.helper:Example.decorated_deep'
