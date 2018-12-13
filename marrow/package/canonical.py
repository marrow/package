from functools import partial
from inspect import getmodule, getmembers, isclass, isroutine
from typeguard import check_argument_types
from typing import Callable


def name(obj) -> str:
	"""This helper function attempts to resolve the dot-colon import path for a given object.
	
	Specifically searches for classes and methods, it should be able to find nearly anything at either the module
	level or nested one level deep.  Uses ``__qualname__`` if available.
	"""
	
	if not isroutine(obj) and not hasattr(obj, '__name__') and hasattr(obj, '__class__'):
		obj = obj.__class__
	
	module = getmodule(obj)
	
	return module.__name__ + ':' + obj.__qualname__
