# encoding: utf-8

from collections import defaultdict

from .loader import load


class PluginCache(defaultdict):
	"""Lazily load plugins from the given namespace."""

	def __init__(self,  namespace):
		super(PluginCache, self).__init__()
		self.namespace =  namespace

	def __missing__(self,  key):
		self[key] = load(key,  self.namespace)
		return self[key]
	
	def __getattr__(self, name):
		return self[name]
