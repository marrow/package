"""Tarjan's algorithm and topological sorting implementation in Python.

by Paul Harrison

Public domain, do with it as you will.

From a blog post by Paul Harrison: http://www.logarithmic.net/pfh/blog/01208083168

Some cleanup was applied, and Python 3 function annotations (typing module, typeguard validation) supplied.
"""

from collections import defaultdict
from typeguard import typechecked
from typing import List, Mapping, MutableMapping, Sequence, Tuple, Iterable

Graph = Mapping[str, Iterable[str]]


@typechecked
def strongly_connected_components(graph: Graph) -> List[Tuple]:
	"""Find the strongly connected components in a graph using Tarjan's algorithm.
	
	The `graph` argument should be a dictionary mapping node names to sequences of successor nodes.
	"""
	
	result: List[Tuple[str, ...]] = []
	stack: List[str] = []
	low: MutableMapping[str, int] = {}
	
	def visit(node: str):
		if node in low: return
		
		num = len(low)
		low[node] = num
		stack_pos = len(stack)
		stack.append(node)
		
		for successor in graph[node]:
			visit(successor)
			low[node] = min(low[node], low[successor])
		
		if num == low[node]:
			component = tuple(stack[stack_pos:])
			del stack[stack_pos:]
			
			result.append(component)
			
			for item in component:
				low[item] = len(graph)
	
	for node in graph:
		visit(node)
	
	return result


@typechecked
def topological_sort(graph:Graph) -> list:
	count: MutableMapping[str, int] = defaultdict(lambda: 0)
	
	for node in graph:
		for successor in graph[node]:
			count[successor] += 1
	
	result = []
	ready = [node for node in graph if count[node] == 0]
	
	while ready:
		node = ready.pop(-1)
		result.append(node)
		
		for successor in graph[node]:
			count[successor] -= 1
			if count[successor] == 0:
				ready.append(successor)
	
	return result


@typechecked
def robust_topological_sort(graph: Graph) -> list:
	"""Identify strongly connected components then perform a topological sort of those components."""
	
	components = strongly_connected_components(graph)
	
	node_component = {}
	component_graph: Graph = {}
	
	for component in components:
		for node in component:
			node_component[node] = component
	
	for component in components:
		component_graph[component] = []
	
	for node in graph:
		node_c = node_component[node]
		
		for successor in graph[node]:
			successor_c = node_component[successor]
			
			if node_c != successor_c:
				component_graph[node_c].append(successor_c) 
	
	return topological_sort(component_graph)
