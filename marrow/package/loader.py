import os

from pkg_resources import iter_entry_points, resource_filename
from typing import Sequence, Optional

from typeguard import check_argument_types


nodefault = object()


def traverse(obj, target:str, default=nodefault, executable:bool=False, separator:str='.', protect:bool=True):
	"""Traverse down an object, using getattr or getitem.
	
	If ``executable`` is ``True`` any executable function encountered will be, with no arguments. Traversal will
	continue on the result of that call.  You can change the separator as desired, i.e. to a '/'.
	
	By default attributes (but not array elements) prefixed with an underscore are taboo.  They will not resolve,
	raising a LookupError.
	
	Certain allowances are made: if a 'path segment' is numerical, it's treated as an array index. If attribute
	lookup fails, it will re-try on that object using array notation and continue from there.  This makes lookup
	very flexible.
	"""
	
	# TODO: Support numerical slicing, i.e. ``1:4``, or even just ``:-1`` and things.
	assert check_argument_types()
	
	value = obj
	remainder = target
	
	if not target:
		return obj
	
	while separator:
		name, separator, remainder = remainder.partition(separator)
		numeric = name.lstrip('-').isdigit()
		
		try:
			if numeric or (protect and name.startswith('_')):
				raise AttributeError()
			
			value = getattr(value, name)
			
			if executable and callable(value):
				value = value()
		
		except AttributeError:
			try:
				value = value[int(name) if numeric else name]
			
			except (KeyError, TypeError):
				if default is nodefault:
					raise LookupError("Could not resolve '" + target + "' on: " + repr(obj))
				
				return default
		
	return value


def load(target:str, namespace:str=None, default=nodefault, executable:bool=False, separators:Sequence[str]=('.', ':', '/'),
		protect:bool=True):
	"""This helper function loads an object identified by a dotted-notation string.
	
	For example::
	
		# Load class Foo from example.objects.
		load('example.objects:Foo')
		
		# Load the result of the class method ``new`` of the Foo object.
		load('example.objects:Foo.new', executable=True)
	
	If a plugin namespace is provided simple name references are allowed.  For example::
	
		# Load the plugin named 'routing' from the 'web.dispatch' namespace.
		load('routing', 'web.dispatch')
	
	The ``executable``, ``protect``, and first tuple element of ``separators`` are passed to the traverse function.
	Providing a namespace does not prevent full object lookup (dot-colon notation) from working.
	
	This can also be used to look up the absolute path to a file relative to a package path. Where dot-colon notation
	will retrieve a named attribute, forward-slash notation will retrieve the path to a file relative to the dot-
	notation package:
	
		# Where is master.html relative to example.template?
		load('example.template/master.html')
	"""
	
	assert check_argument_types()
	path:Optional[str] = None
	
	if separators[1] in target and separators[2] in target:
		raise LookupError("Can not target an attribute from a file on-disk.")
	
	if namespace and separators[1] not in target:
		allowable = dict((i.name,  i) for i in iter_entry_points(namespace))
		
		if target not in allowable:
			raise LookupError('Unknown plugin "' + target + '"; found: ' + ', '.join(allowable))
		
		return allowable[target].load()
	
	if separators[2] in target:
		target, _, path = target.partition(separators[2])
		
		if not target or not path:
			raise LookupError("Must specify a target package and package-relative path.")
		
		path = path.replace('/', os.path.sep)  # Adapt to platform conventions.
		path = resource_filename(target, path)
		
		return path
	
	parts, _, target = target.partition(separators[1])
	
	try:
		obj = __import__(parts)
	except ImportError:
		if default is not nodefault:
			return default
		
		raise
	
	return traverse(
			obj,
			separators[0].join(parts.split(separators[0])[1:] + target.split(separators[0])),
			default = default,
			executable = executable,
			protect = protect
		) if target else obj
