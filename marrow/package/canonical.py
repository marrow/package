# encoding: utf-8

from __future__ import unicode_literals

from inspect import getmodule, getmembers, isclass, isroutine


def search(parent, obj, path=''):  # pragma: no cover - used on Python < 3.3 only
	if obj == parent.__dict__.get(obj.__name__, None) or obj == getattr(parent, obj.__name__, None):
		return path + ('.' if path else '') + obj.__name__
	
	if path:
		# We don't want to recurse forever... one level is good.
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
	except AttributeError:  # pragma: no cover - used on Python < 3.3 only
		pass
	
	# This should handle all method combinations.
	if hasattr(obj, '__func__'):  # pragma: no cover - used on Python < 3.3 only
		if hasattr(obj, '__self__') and isclass(obj.__self__):
			return module.__name__ + ':' + search(module, obj.__self__) + '.' + obj.__name__
		
		obj = obj.__func__
	
	# Final hope.  Search.
	return module.__name__ + ':' + search(module, obj)  # pragma: no cover - used on Python < 3.3 only
