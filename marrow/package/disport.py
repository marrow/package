"""Import redirector registry utility.

Disport; noun: diversion from work or serious matters; recreation or amusement.
"""

from collections import deque
from typeguard import typechecked
from typing import Deque, Sequence, Iterable, Optional

from .loader import load, nodefault


class Importer:
	"""A helper class to redirect imports and plugin loading.
	
	Predominantly useful when paired with a template importer such as web.template or import-based template engine
	like cinje to allow for overriding of page components.
	
	Later overrides take precedence over earlier ones, and are evaluated using a prefix search to construct a list of
	candidate import paths. Each is attempted until one succeeds, or none succeed, at which point the original import
	is attempted.
	
	Plugin names can be overridden as well, however, the destination should still be a module path. The object name
	referenced by the original entry_point will be attempted against the overridden path, with similar fallback to the
	original.
	"""
	
	__slots__ = ('redirects', 'namespace', 'separators', 'executable', 'protect')
	
	redirects: Deque[str]
	namespace: str
	separators: Iterable[str]
	executable: bool
	protect: bool
	
	@typechecked
	def __init__(self, redirect:Optional[Iterable[str]]=None, namespace:str=None,
				separators:Iterable[str]=('.', ':'), executable:bool=False, protect:bool=True):
		"""Configure the disport Importer.
		
		The arguments are essentially the same as those for the load or lazyload utilities, with the addition of the
		ability to specify an initial iterable of overrides through the `redirect` argument. This should be an
		iterable of tuples (or tuple-alikes) in the form `(source, destination)`.
		"""
		
		super().__init__()
		
		self.redirects = deque()
		self.namespace = namespace
		self.separators = separators
		self.executable = executable
		self.protect = protect
		
		# Initial redirects processing.
		if redirect:
			for source, destination in redirect:
				self.redirect(source, destination)
	
	@typechecked
	def redirect(self, source:str, destination:str):
		self.redirects.appendleft((source, destination))
	
	@typechecked
	def __call__(self, target:str, default=nodefault):
		for candidate, destination in self.redirects:
			if candidate == target:  # Plugin reference.
				pass
				return
			
			if not target.startswith(candidate):
				continue
			
			# Prefix match found, attempt import.
			candidate = load(
					target.replace(candidate, destination, 1),
					namespace = self.namespace,
					default = None,
					executable = self.executable,
					separators = self.separators,
					protect = self.protect
				)
			
			if candidate is not None:
				return candidate
		
		# Fall back on direct use.
		return load(
				target.replace(candidate, destination),
				namespace = self.namespace,
				default = default,
				executable = self.executable,
				separators = self.separators,
				protect = self.protect
			)
