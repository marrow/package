# encoding: utf-8

from __future__ import unicode_literals

from functools import partial
from inspect import getmodule, getmembers, isclass, isroutine


def unwrap(obj, attr='__wrapped__'):
	"""Handle the @functools.wrap decorator protocol, determining the originally wrapped function."""
	
	while hasattr(obj, attr):
		obj = getattr(obj, attr)
	
	return obj


def search(parent, obj, path=''):
	obj = unwrap(unwrap(obj), '__func__')
	
	candidates = [
			partial(parent.__dict__.get, obj.__name__, None),
			partial(getattr, parent, obj.__name__, None)
		]
	
	for candidate in candidates:
		candidate = unwrap(unwrap(candidate()), '__func__')
		if obj is candidate or obj == candidate:
			return path + ('.' if path else '') + obj.__name__
		
	if path:
		# We don't want to recurse forever... one level is acceptable for most applications.
		# If you need deeper inspection, use Python 3.3+ for __qualname__ support.
		raise LookupError("Can not identify canonical name for object: " + repr(obj))
	
	for name, member in getmembers(parent, isclass):
		try:
			return search(member, obj, name)
		except LookupError:
			pass
	
	raise LookupError("Can not identify canonical name for object: " + repr(obj))


def name(obj):
	"""This helper function attempts to resolve the dot-colon import path for a given object.
	
	Specifically searches for classes and methods, it should be able to find nearly anything at either the module
	level or nested one level deep.  Uses ``__qualname__`` if available.
	"""
	
	if not isroutine(obj) and not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	module = getmodule(obj)
	
	try:
		# Short-cut for Python 3.3+
		return module.__name__ + ':' + obj.__qualname__
	except AttributeError:
		pass
	
	# This should handle all method combinations.
	if hasattr(obj, '__func__'):
		if hasattr(obj, '__self__') and isclass(obj.__self__):
			return module.__name__ + ':' + search(module, obj.__self__) + '.' + obj.__name__
		
		obj = obj.__func__
	
	# Final hope.  Search.
	return module.__name__ + ':' + search(module, obj)
