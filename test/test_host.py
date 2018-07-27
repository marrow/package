# encoding: utf-8

import pytest

from unittest import TestCase

from marrow.package.host import ExtensionManager

from pip._internal import main as pip


class BadExtension(object):
	needs = ('nan', )

class AExtension(object):
	provides = ('a', )
	needs = ()

class BExtension(object):
	provides = ('b', )
	needs = ('a', )

class CExtension(object):
	needs = ('a', )

class DExtension(object):
	needs = ('b', )

class EExtension(object):
	first = True

class FExtension(object):
	last = True

class GExtension(object):
	provides = ('g', )
	needs = ('h', )

class HExtension(object):
	provides = ('h', )
	needs = ('g', )

class XExtension(object):
	provides = ('x', )
	excludes = ('a', )


class TestExtensionManager(TestCase):
	def test__plugin__access_via_attribute(self):
		assert ExtensionManager('console_scripts').pip is pip
	
	def test__plugin__access_via_array(self):
		assert ExtensionManager('console_scripts')['pip'] is pip
	
	def test__plugin__registry(self):
		manager = ExtensionManager('console_scripts')
		
		extensions = [AExtension(), BExtension(), CExtension()]
		
		manager.register('foo', extensions[0])
		manager.register('bar', extensions[1])
		manager.register('baz', extensions[2])
		
		assert extensions[0] in extensions
		assert extensions[1] in extensions
		assert extensions[2] in extensions
		
		assert extensions[0] in [i for i in manager]
	
	def test__extension__fails_not_existant_need(self):
		manager = ExtensionManager('console_scripts')
		
		with pytest.raises(LookupError):
			manager.order([BadExtension()])
	
	def test__extension__resolve_chain(self):
		manager = ExtensionManager('console_scripts')
		
		extensions = [AExtension(), BExtension(), DExtension()]
		
		assert manager.order(extensions) == extensions
		assert manager.order([i for i in reversed(extensions)]) == extensions
	
	def test__extension__equal_need(self):
		manager = ExtensionManager('console_scripts')
		
		extensions = [AExtension(), BExtension(), CExtension()]
		
		# This test suffers from a small amount of entropy.
		assert manager.order(extensions) in (extensions, [extensions[0], extensions[2], extensions[1]])
	
	def test__extension__first_and_last(self):
		manager = ExtensionManager('console_scripts')
		
		extensions = [EExtension(), AExtension(), FExtension()]
		
		assert manager.order(extensions) == extensions
	
	def test__extension__circular_need(self):
		manager = ExtensionManager('console_scripts')
		
		with pytest.raises(LookupError):
			manager.order([GExtension(), HExtension()])
	
	def test__extension__exclusion(self):
		manager = ExtensionManager('console_scripts')
		
		with pytest.raises(RuntimeError):
			manager.order([AExtension(), XExtension()])
