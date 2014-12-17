# encoding: utf-8

from __future__ import unicode_literals, print_function

from functools import wraps


def simple_decorator(fn):
	@wraps(fn)
	def inner(*args, **kw):
		return fn(*args, **kw)
	
	return inner


def bare():
	def closure():
		pass
	
	return closure


@simple_decorator
def decorated_shallow():
	pass


@simple_decorator
@simple_decorator
def decorated_deep():
	pass


class Example(object):
	class Pandora(object):
		class Box(object):
			def nested(self):
				pass
		
		def nested(self):
			pass
	
	def instance(self):
		return self
	
	@classmethod
	def classmethod(cls):
		return cls
	
	@staticmethod
	def staticmethod():
		pass
	
	@simple_decorator
	def decorated_shallow(self):
		pass
	
	@simple_decorator
	@simple_decorator
	def decorated_deep(self):
		pass

instance = Example()


def main():
	# We run some tests and output the results.
	
	import re
	from inspect import getmembers, ismodule, isclass, ismethod, isfunction, isroutine
	
	addrstrip = re.compile(r' at 0x[0-9a-fA-F]+')
	
	sources = [('class', Example), ('instance', instance)]
	functions = ['instance', 'classmethod', 'staticmethod']
	attributes = ['__name__', '__class__', '__module__', '__func__', '__self__', 'im_self', 'im_class', '__qualname__']
	calls = [ismodule, isclass, ismethod, isfunction, isroutine]
	extras = [('bare_fn', bare), ('closure', bare()), ('bare_cls', Example), ('bare_inst', instance), ('nested', Example.Pandora), ('deep', Example.Pandora.Box)]
	
	print('Expected Candidate Attributes\n\nSource', 'Function', 'Attribute', 'Value', sep='\t')
	
	missing = object()
	
	for sname, source in sources:
		for function in functions:
			src = getattr(source, function)
			for attribute in attributes:
				value = getattr(src, attribute, missing)
				print(sname, function, attribute, '-' if value is missing else addrstrip.sub('', repr(value)), sep='\t')
			for call in calls:
				print(sname, function, call.__name__ + '()', call(src), sep='\t')
	
	for ename, extra in extras:
		for attribute in attributes:
			value = getattr(extra, attribute, missing)
			print('direct', ename, attribute, '-' if value is missing else addrstrip.sub('', repr(value)), sep='\t')
		for call in calls:
			print('direct', ename, call.__name__ + '()', call(extra), sep='\t')
	
	print('\n\nAll Candidate Attributes\n\nSource', 'Function', 'Member', 'Value', sep='\t')
	
	def callback(obj):
		# Evaluate; what exactly are we looking for?
		# if isclass(obj): return True
		
		for i in (Example, Example.Pandora, Example.Pandora.Box, Example.Pandora.Box.nested, Example.Pandora.nested, Example.instance, Example.classmethod, Example.staticmethod, instance.instance, instance.classmethod, instance.staticmethod, instance):
			if obj is i or obj == i: return True
			if hasattr(i, '__name__') and i.__name__ in repr(obj): return True
			
		return False
	
	for sname, source in sources:
		for function in functions:
			src = getattr(source, function)
			
			for name, value in getmembers(src, callback):
				if name == '__globals__': continue
				print(sname, function, name, addrstrip.sub('', repr(value)), sep='\t')

if __name__ == '__main__':
	main()
