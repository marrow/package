# encoding: utf-8

from threading import RLock
from collections import MutableMapping


sentinel = object()


class lazy(object):
	"""Lazily record the result of evaluating a function and cache the result.
	
	This is a non-data descriptor which tells Python to allow the instance __dict__ to override.
	"""
	
	def __init__(self, func, name=None, doc=None):
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