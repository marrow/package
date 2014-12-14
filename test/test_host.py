# encoding: utf-8

import pytest

from unittest import TestCase

from marrow.package.host import ExtensionManager

#from test import helper


class TestExtensionManager(TestCase):
	class Extension(object):
		needs = ('nan', )
	
	def test__manager__fails_not_existant_need(self):
		manager = ExtensionManager('console_scripts')
		
		with pytest.raises(LookupError):
			manager.order([self.Extension()])
