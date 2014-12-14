# encoding: utf-8

import os
import pkg_resources

from collections import defaultdict

from .cache import PluginCache
from .loader import traverse
from .tarjan import robust_topological_sort


log = __import__('logging').getLogger(__name__)


class PluginManager(object):
	def __init__(self, namespace, folders=None):
		self.namespace = namespace
		self.folders = folders if folders else list()
		self.plugins = list()
		self.named = PluginCache(namespace)
		
		self.ws = ws = pkg_resources.working_set
		
		for container in self.folders:  # pragma: no cover - TODO: Figure out how to test this.
			path = os.path.abspath(os.path.expanduser(container))
			log.info("Adding " + path + " to plugin search path.")
			ws.add_entry(path)
			env = pkg_resources.Environment([path])
			ws.require(*env)
		
		ws.subscribe(self._register)
		
		super(PluginManager, self).__init__()
	
	def register(self, name, plugin):
		log.info("Registering plugin: %s %r", name, plugin)
		self.named[name] = plugin
		self.plugins.append(plugin)
	
	def _register(self, dist):
		entries = dist.get_entry_map(self.namespace)
		
		if not entries:
			return
		
		try:
			for name in entries:
				plugin = entries[name].load()
				
				self.register(name, plugin)
		
		except pkg_resources.UnknownExtra:  # pragma: no cover - TODO: Figure out how to test this.
			pass # skipping plugin due to missing dependencies
		
		except ImportError:  # pragma: no cover - TODO: Figure out how to test this.
			pass # skipping plugin due to malformed import
	
	def __iter__(self):
		for plugin in self.plugins:
			yield plugin
	
	def __getattr__(self, name):
		return self.named[name]
	
	def __getitem__(self, name):
		return self.named[name]


class ExtensionManager(PluginManager):
	"""More advanced plugin architecture using structured "extensions".
	
	Extensions describe their dependencies using an expressive syntax:
	
	* ``provides`` — declare tags describing the features offered by the plugin
	* ``needs`` — delcare the tags that must be present for this extension to function
	* ``uses`` — declare the tags that must be evaluated prior to this extension, but aren't hard requirements
	* ``first`` — declare that this extension is a dependency of all other non-first extensions
	* ``last`` — declare that this extension depends on all other non-last extensions
	
	"""
	
	def order(self, config=None, prefix=''):
		extensions = traverse(config if config else self.plugins, prefix)
		
		# First, we check that everything absolutely required is configured.
		
		provided = set().union(*(traverse(ext, 'provides', ()) for ext in extensions))
		needed = set().union(*(traverse(ext, 'needs', ()) for ext in extensions))
		
		if not provided.issuperset(needed):
			raise LookupError("Extensions providing the following features must be configured:\n" + \
					', '.join(needed.difference(provided)))
		
		# Now we spider the configured extensions and graph them.  This is a multi-step process.
		
		# First, create a mapping of feature names to extensions.  We only want extension objects in our initial graph.
		
		universal = list()  # these always go first (in alphabetical order)
		inverse = list()  # these always go last (in reverse alphabetical order)
		provides = dict()
		
		universal.sort()
		inverse.sort(reverse=True)
		
		for ext in extensions:
			for feature in traverse(ext, 'provides', ()):
				provides[feature] = ext
			
			if traverse(ext, 'first', False):
				universal.append(ext)
			elif traverse(ext, 'last', False):
				inverse.append(ext)
		
		# Now we build the initial graph.
		
		dependencies = dict()
		
		for ext in extensions:
			# We build a set of requirements from needs + uses that have been fulfilled.
			requirements = set(traverse(ext, 'needs', ()))
			requirements.update(set(traverse(ext, 'uses', ())).intersection(provided))
			
			dependencies[ext] = set(provides[req] for req in requirements)
			
			if universal and ext not in universal:
				dependencies[ext].update(universal)
			
			if inverse and ext in inverse:
				dependencies[ext].update(set(extensions).difference(inverse))
		
		# Build the final "unidirected acyclic graph"; a list of extensions in dependency-resolved order.
		dependencies = robust_topological_sort(dependencies)
		
		# If there are any tuple elements, we've got a circular reference!
		extensions = []
		for ext in dependencies:
			if len(ext) > 1:
				raise LookupError("Circular dependency found: " + repr(ext))
			
			extensions.append(ext[0])
		
		extensions.reverse()
		
		return extensions
	
	
