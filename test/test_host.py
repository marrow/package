import pytest

from unittest import TestCase

from marrow.package import name, load
from marrow.package.host import ExtensionManager


class BadExtension:
	needs = ('nan', )

class AExtension:
	provides = ('a', )
	needs = ()

class BExtension:
	provides = ('b', )
	needs = ('a', )

class CExtension:
	needs = ('a', )

class DExtension:
	needs = ('b', )

class EExtension:
	first = True

class FExtension:
	last = True

class GExtension:
	provides = ('g', )
	needs = ('h', )

class HExtension:
	provides = ('h', )
	needs = ('g', )

class XExtension:
	provides = ('x', )
	excludes = ('a', )


class TestExtensionManager(TestCase):
	def test__plugin__access_via_attribute(self):
		assert ExtensionManager('marrow.package.sample').load is load
	
	def test__plugin__access_via_array(self):
		assert ExtensionManager('marrow.package.sample')['name'] is name
	
	def test__plugin__registry(self):
		manager = ExtensionManager('marrow.package.sample')
		
		extensions = [AExtension(), BExtension(), CExtension()]
		
		manager.register('foo', extensions[0])
		manager.register('bar', extensions[1])
		manager.register('baz', extensions[2])
		
		assert extensions[0] in extensions
		assert extensions[1] in extensions
		assert extensions[2] in extensions
		
		assert extensions[0] in [i for i in manager]
	
	def test__extension__fails_not_existant_need(self):
		manager = ExtensionManager('marrow.package.sample')
		
		with pytest.raises(LookupError):
			manager.order([BadExtension()])
	
	def test__extension__resolve_chain(self):
		manager = ExtensionManager('marrow.package.sample')
		
		extensions = [AExtension(), BExtension(), DExtension()]
		
		assert manager.order(extensions) == extensions
		assert manager.order([i for i in reversed(extensions)]) == extensions
	
	def test__extension__equal_need(self):
		manager = ExtensionManager('marrow.package.sample')
		
		extensions = [AExtension(), BExtension(), CExtension()]
		
		# This test suffers from a small amount of entropy.
		assert manager.order(extensions) in (extensions, [extensions[0], extensions[2], extensions[1]])
	
	def test__extension__first_and_last(self):
		manager = ExtensionManager('marrow.package.sample')
		
		extensions = [EExtension(), AExtension(), FExtension()]
		
		assert manager.order(extensions) == extensions
	
	def test__extension__circular_need(self):
		manager = ExtensionManager('marrow.package.sample')
		
		with pytest.raises(LookupError):
			manager.order([GExtension(), HExtension()])
	
	def test__extension__exclusion(self):
		manager = ExtensionManager('marrow.package.sample')
		
		with pytest.raises(RuntimeError):
			manager.order([AExtension(), XExtension()])
