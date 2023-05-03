from collections import defaultdict
from typeguard import typechecked

from .loader import load


class PluginCache(defaultdict):
	"""Lazily load plugins from the given namespace.
	
	Supports read-only dictionary-like and attribute access.
	"""
	
	@typechecked
	def __init__(self,  namespace: str):
		"""You must specify an entry point namespace."""
		
		super().__init__()
		
		self.namespace =  namespace
	
	def __missing__(self,  key):
		"""If not already loaded, attempt to load the reference."""
		
		self[key] = load(key, self.namespace)
		return self[key]
	
	def __getattr__(self, name):
		"""Proxy attribute access through to the dictionary."""
		
		try:
			return self[name]
		except KeyError:
			pass
		
		raise AttributeError()
