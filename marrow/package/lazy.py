from threading import RLock
from collections.abc import MutableMapping
from typeguard import check_argument_types
from typing import Callable

from .loader import traverse, load


sentinel = object()


class lazy:
	"""Lazily record the result of evaluating a function and cache the result.
	
	This is a non-data descriptor which tells Python to allow the instance `__dict__` to override, naturally caching
	the result. As a consequence of this assignment, whatever name is given to the lazy property must be included in
	the class' `__slots__` declaration, if one is given.
	
	Use as a decorator just like `@property`:
	
		class MyClass:
			@lazy
			def myattr(self):
				print("Executed!")
				return 42
		
		obj = MyClass()
		assert obj.myattr == 42 # Executed!
		assert obj.myattr == 42 # Not.
	"""
	
	def __init__(self, func:Callable[[object], None], name:str=None, doc:str=None):
		assert check_argument_types()
		
		self.__name__ = name or func.__name__
		self.__module__ = func.__module__
		self.__doc__ = func.__doc__
		self.lock = RLock()
		self.func = func
	
	def __repr__(self):
		return "lazy(" + repr(self.func) + ")"
	
	def __get__(self, instance, type=None):
		if instance is None:  # Allow direct access to the non-data descriptor via the class.
			return self
		
		with self.lock:  # Try to avoid situations with parallel thread access hammering the function.
			value = instance.__dict__.get(self.__name__, sentinel)
			
			if value is sentinel:
				value = instance.__dict__[self.__name__] = self.func(instance)
		
		return value


def lazyload(reference: str, *args, **kw):
	"""Lazily load and cache an object reference upon dereferencing.
	
	Assign the result of calling this function with either an object reference passed in positionally:
	
		class MyClass:
			debug = lazyload('logging:debug')
	
	Or the attribute path to traverse (using `marrow.package.loader:traverse`) prefixed by a period.
	
		class AnotherClass:
			target = 'logging:info'
			log = lazyload('.target')
	
	Additional arguments are passed to the eventual call to `load()`.
	"""
	
	assert check_argument_types()
	
	def lazily_load_reference(self):
		ref = reference
		
		if ref.startswith('.'):
			ref = traverse(self, ref[1:])
		
		return load(ref, *args, **kw)
	
	return lazy(lazily_load_reference)
