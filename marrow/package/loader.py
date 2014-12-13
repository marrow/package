# encoding: utf-8

from .release import version as __version__


def load(target, namespace=None):
	"""This helper function loads an object identified by a dotted-notation string.
	
	For example::
	
		# Load class Foo from example.objects
		load('example.objects:Foo')
	
	If a plugin namespace is provided simple name references are allowed.  For example::
	
		# Load the plugin named 'routing' from the 'web.dispatch' namespace
		load('routing', 'web.dispatch')
	
	Providing a namespace does not prevent full object lookup (dot-colon notation) from working.
	"""
	if namespace and ':' not in target:
		if not iter_entry_points:
			raise ImportError("Unable to import pkg_resources; do you have setuptools installed?")
		
		allowable = dict((i.name,  i) for i in iter_entry_points(namespace))
		if target not in allowable:
			raise ValueError('Unknown plugin "' + target + '"; found: ' + ', '.join(allowable))
		return allowable[target].load()
	
	parts, target = target.split(':') if ':' in target else (target, None)
	obj = __import__(parts)
	
	for part in chain(parts.split('.')[1:], target.split('.') if target else []):
		obj = getattr(obj, part)
		
		return obj
