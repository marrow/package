import os
import pkg_resources

from typeguard import check_argument_types
from typing import Sequence
from pkg_resources import Distribution

from .canonical import name as _name
from .cache import PluginCache
from .loader import traverse
from .tarjan import robust_topological_sort


log = __import__('logging').getLogger(__name__)


class PluginManager:
	def __init__(self, namespace:str, folders:Sequence[str]=None):
		assert check_argument_types()
		
		self.namespace = namespace
		self.folders = folders if folders else list()
		self.plugins = list()
		self.named = PluginCache(namespace)
		
		self.ws = ws = pkg_resources.working_set
		
		for container in self.folders:  # pragma: no cover - TODO: Figure out how to test this.
			path = os.path.abspath(os.path.expanduser(container))
			log.info("Adding " + path + " to plugin search path.", extra=dict(path=path, namespace=self.namespace))
			ws.add_entry(path)
			env = pkg_resources.Environment([path])
			ws.require(*env)
		
		ws.subscribe(self._register)
		
		super(PluginManager, self).__init__()
	
	def register(self, name:str, plugin:object) -> None:
		assert check_argument_types()
		
		log.info("Registering plugin" + name + " in namespace " + self.namespace + ".",
				extra = dict(plugin_name=name, namespace=self.namespace, plugin=_name(plugin)))
		self.named[name] = plugin
		self.plugins.append(plugin)
	
	def _register(self, dist:Distribution) -> None:
		assert check_argument_types()
		entries = dist.get_entry_map(self.namespace)
		
		if not entries:
			return
		
		try:
			for name in entries:
				plugin = entries[name].load()
				
				self.register(name, plugin)
		
		except pkg_resources.UnknownExtra:  # pragma: no cover - TODO: Figure out how to test this.
			log.warning("Skipping registration of '{!r}' due to missing dependencies.".format(dist), exc_info=True)
		
		except ImportError:  # pragma: no cover - TODO: Figure out how to test this.
			log.error("Skipping registration of '{!r}' due to uncaught error on import.".format(dist), exc_info=True)
	
	def __iter__(self):
		for plugin in self.plugins:
			yield plugin
	
	def __getattr__(self, name:str):
		return self.named[name]
	
	def __getitem__(self, name:str):
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
		
		universal = list()
		inverse = list()
		provides = dict()
		excludes = dict()
		
		for ext in extensions:
			for feature in traverse(ext, 'provides', ()):
				provides[feature] = ext
			
			for feature in traverse(ext, 'excludes', ()):
				excludes.setdefault(feature, []).append(ext)
			
			if traverse(ext, 'first', False):
				universal.append(ext)
			elif traverse(ext, 'last', False):
				inverse.append(ext)
		
		# We bail early if there are known conflicts up-front.
		
		for conflict in set(provides) & set(excludes):
			raise RuntimeError("{!r} precludes use of '{!s}', which is defined by {!r}".format(
					excludes[conflict], conflict, provides[conflict]))
		
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
