from inspect import getmodule, isroutine


def name(obj) -> str:
	"""Resolve the dot-colon import path for a given object as suitable for subsequent use with `lookup`."""
	
	if not isroutine(obj) and not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	module = getmodule(obj)
	
	if module is None:
		raise LookupError("Unable to identify module for: " + repr(obj))
	
	return module.__name__ + ':' + obj.__qualname__
