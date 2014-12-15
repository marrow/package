# encoding: utf-8

from __future__ import unicode_literals

import pytest

from unittest import TestCase

from marrow.package.tarjan import strongly_connected_components, topological_sort, robust_topological_sort

scc = strongly_connected_components
ts = topological_sort
rtc = robust_topological_sort


class TestTarjan(TestCase):
	GOOD = dict(foo=['bar'], bar=[], baz=['foo'])
	BAD = dict(foo=['bar'], bar=['baz'], baz=['bar'])
	MISSING = dict(foo=['bar'], bar=['baz'])
	
	def test_strongly_connected_components_good(self):
		# standard (no tricks) dependency graph
		assert scc(self.GOOD) == [('bar', ), ('foo', ), ('baz', )]
	
	def test_strongly_connected_components_bad(self):
		# baz and bar depend on each-other
		assert [tuple(sorted(i)) for i in scc(self.BAD)] == [('bar', 'baz'), ('foo', )]
	
	def test_strongly_connected_components_ugly(self):
		# a dependency is missing so we explode
		with pytest.raises(KeyError):
			scc(self.MISSING)
	
	def test_topological_sort_good(self):
		# resolved from most dependent to least
		assert ts(self.GOOD) == ['baz', 'foo', 'bar']
	
	def test_topological_sort_bad(self):
		# only resolvable items are returned
		assert ts(self.BAD) == ['foo']
	
	def test_topological_sort_ugly(self):
		with pytest.raises(KeyError):
			ts(self.MISSING)
	
	def test_robust_topological_sort_good(self):
		# return parallel sets from least to most dependent
		assert rtc(self.GOOD) == [('baz', ), ('foo', ), ('bar', )]

	def test_robust_topological_sort_bad(self):
		# like the strongly connected components, but reversed
		assert [tuple(sorted(i)) for i in rtc(self.BAD)] == [('foo', ), ('bar', 'baz')]

	def test_robust_topological_sort_ugly(self):
		# as per the other ugly cases, we expect to bomb
		with pytest.raises(KeyError):
			rtc(self.MISSING)
