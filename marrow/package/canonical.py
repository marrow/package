# encoding: utf-8

from __future__ import unicode_literals

from inspect import getmodule, getmembers, isclass, isfunction, ismethod, isroutine


def search(parent, obj):
	pass




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
	
	
	
	raise LookupError("Can not identify canonical name for object: " + repr(obj))
	
	
	
	
	
	
	if not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	q = getattr(obj, '__qualname__', None)
	
	if not q:
		q = obj.__name__
		
		if hasattr(obj, 'im_class'):
			q = obj.im_class.__name__ + '.' + q
			
			return getmodule(obj).__name__ + ':' + q
