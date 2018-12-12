from unittest import TestCase
from pytest import main as pytest
from coverage.cmdline import main as coverage
from pip._internal import main as pip

from marrow.package.cache import PluginCache


class TestPluginCache(TestCase):
	candidates = ('py.test', 'coverage', 'pip')
	
	def test__cache__loads_expected_objects(self):
		cache = PluginCache('console_scripts')
		for candidate, obj in zip(self.candidates, (pytest, coverage, pip)):
			assert cache[candidate] is obj
	
	def test__cache__attribute_access(self):
		cache = PluginCache('console_scripts')
		assert cache.coverage is coverage
	
	def test__cache__actually_caches_things(self):
		cache = PluginCache('console_scripts')
		assert len(cache) == 0
		assert 'coverage' not in cache
		assert cache.coverage is coverage
		assert len(cache) == 1
		assert 'coverage' in cache
