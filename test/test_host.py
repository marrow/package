# encoding: utf-8

import pytest

from unittest import TestCase

from marrow.package.host import ExtensionManager

#from test import helper



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


class TestExtensionManager(TestCase):
	def test__manager__fails_not_existant_need(self):
		manager = ExtensionManager('console_scripts')
		
		with pytest.raises(LookupError):
			manager.order([BadExtension()])
	
	def test__manager__resolve_chain(self):
		manager = ExtensionManager('console_scripts')
		
		extensions = [AExtension(), BExtension(), DExtension()]
		
		assert manager.order(extensions) == extensions
		assert manager.order([i for i in reversed(extensions)]) == extensions
	
	def  test__manager__equal_need(self):
		manager = ExtensionManager('console_scripts')
		
		extensions = [AExtension(), BExtension(), CExtension()]
		
		# This test suffers from a small amount of entropy.
		assert manager.order(extensions) in (extensions, [extensions[0], extensions[2], extensions[1]])
