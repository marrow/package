"""Tarjan's algorithm and topological sorting implementation in Python.

by Paul Harrison

Public domain, do with it as you will.

From a blog post by Paul Harrison: http://www.logarithmic.net/pfh/blog/01208083168

Somee cleanup was applied, and Python 3 function annotations (typing module, typeguard validation) supplied.
"""

from collections import defaultdict
from typeguard import check_argument_types
from typing import List, Mapping, Sequence

Graph = Mapping[str, Sequence[str]]


def strongly_connected_components(graph: Graph) -> List:
	"""Find the strongly connected components in a graph using Tarjan's algorithm.
	
	The `graph` argument should be a dictionary mapping node names to sequences of successor nodes.
	"""
	
	assert check_argument_types()
	
	result = []
	stack = []
	low = {}
	
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


def topological_sort(graph: Graph) -> list:
	assert check_argument_types()
	
	count = defaultdict(lambda: 0)
	
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


def robust_topological_sort(graph: Graph) -> list:
	"""Identify strongly connected components then perform a topological sort of those components."""
	
	assert check_argument_types()
	
	components = strongly_connected_components(graph)
	
	node_component = {}
	for component in components:
		for node in component:
			node_component[node] = component
	
	component_graph = {}
	for component in components:
		component_graph[component] = []
	
	for node in graph:
		node_c = node_component[node]
		for successor in graph[node]:
			successor_c = node_component[successor]
			if node_c != successor_c:
				component_graph[node_c].append(successor_c) 
	
	return topological_sort(component_graph)
