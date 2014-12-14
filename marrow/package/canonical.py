# encoding: utf-8

from __future__ import unicode_literals

from inspect import getmodule, getmembers, isclass, isfunction, ismethod, isroutine


def search(parent, obj, path=''):
	if obj == parent.__dict__.get(obj.__name__, None) or obj == getattr(parent, obj.__name__, None):
		return path + ('.' if path else '') + obj.__name__
	
	if path:
		# We don't want to recurse forever... one level is good.
		raise LookupError("Can not identify canonical name for object: " + repr(obj))
	
	for name, member in getmembers(parent, isclass):
		try:
			return search(member, obj, path + ('.' if path else '') + name)
		except LookupError:
			pass
	
	raise LookupError("Can not identify canonical name for object: " + repr(obj))




def name(obj):
	"""This helper function attempts to resolve the dot-colon import path for the given object.
	
	This is the inverse of 'lookup', which will turn the dot-colon path back into the object.
	
	Python 3.3 added a substantially improved way of determining the fully qualified name for objects;
	this updated method will be used if available.  Note that running earlier versions will prevent correct
	association of nested objects (i.e. objects not at the top level of a module).
	"""
	
	if not isroutine(obj) and not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	module = getmodule(obj)
	
	qcls = isclass(obj)
	qfunc = isfunction(obj)
	qmeth = ismethod(obj)
	
	try:
		# Short-cut for Python 3.3+
		return module.__name__ + ':' + obj.__qualname__
	except AttributeError:
		pass
	
	# Nothing for it but to search for classes if __qualname__ is missing.  :/
	if isclass(obj):
		return module.__name__ + ':' + search(module, obj)
	
	# Python 3.2 goodness.
	if hasattr(obj, '__func__'):
		if hasattr(obj, '__self__') and isclass(obj.__self__):
			return module.__name__ + ':' + search(module, obj.__self__) + '.' + obj.__name__
		
		obj = obj.__func__
	
	
	
	# Try searching, maybe?
	return module.__name__ + ':' + search(module, obj)
	
	raise LookupError("Can not identify canonical name for object: " + repr(obj))
	
	
	
	
	
	
	if not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	q = getattr(obj, '__qualname__', None)
	
	if not q:
		q = obj.__name__
		
		if hasattr(obj, 'im_class'):
			q = obj.im_class.__name__ + '.' + q
			
			return getmodule(obj).__name__ + ':' + q
