from inspect import getmodule, isroutine
from pkg_resources import iter_entry_points
from typing import Optional


def name(obj, namespace:Optional[str]=None, direct:bool=False) -> str:
	"""Resolve the dot-colon import path for a given object as suitable for subsequent use with `lookup`.
	
	If the name of a namespace is provided, the name of the plugin registration for the target object is returned. If
	a plugin can not be identified for the target object a LookupError will be raised, unless "direct" is truthy.
	"""
	
	if not isroutine(obj) and not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	module = getmodule(obj)
	
	if module is None:
		raise LookupError("Unable to identify module for: " + repr(obj))
	
	name = module.__name__ + ':' + obj.__qualname__
	
	if namespace:
		eps = list(iter_entry_points(namespace))
		for ep in eps:
			candidate = ep.module_name + ':' + ep.attrs[0]
			if candidate == name:
				name = ep.name
				break
		else:
			if not direct: raise LookupError("Plugin not found for object: " + name)
	
	return name
