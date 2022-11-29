import pytest

from marrow.package import load, name, traverse
from marrow.package.cache import PluginCache


class TestCache:
	pairs = (
			('name', name),
			('load', load),
			('traverse', traverse),
		)
	
	@pytest.mark.parametrize("name,obj", pairs)
	def test__cache__loads_expected_objects(self, name, obj):
		cache = PluginCache('marrow.package.sample')
		assert cache[name] == obj
	
	def test__cache__attribute_access(self):
		cache = PluginCache('marrow.package.sample')
		assert cache.traverse is traverse
	
	def test__cache__actually_caches_things(self):
		cache = PluginCache('marrow.package.sample')
		assert len(cache) == 0
		assert 'load' not in cache
		assert cache.load is load
		assert len(cache) == 1
		assert 'load' in cache

