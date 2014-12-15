# encoding: utf-8

from collections import defaultdict

from .loader import load


class PluginCache(defaultdict):
	"""Lazily load plugins from the given namespace.
	
	Supports dictionary-style and read-only attribute access.
	"""

	def __init__(self,  namespace):
		"""You must specify an entry point namespace."""
		
		super(PluginCache, self).__init__()
		self.namespace =  namespace

	def __missing__(self,  key):
		"""If not already loaded, attempt to load the reference."""
		
		self[key] = load(key, self.namespace)
		return self[key]
	
	def __getattr__(self, name):
		"""Proxy attribute access through to the dictionary."""
		
		return self[name]
