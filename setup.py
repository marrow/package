#!/usr/bin/env python3

import codecs
import os
import sys

from setuptools import setup


if sys.version_info < (3, 4):
	raise SystemExit("Python 3.4 or later is required.")

exec(open(os.path.join("marrow", "package", "release.py")).read())

here = os.path.abspath(os.path.dirname(__file__))

tests_require = ['pytest', 'pytest-cov', 'pytest-flakes']


setup(
	name = "marrow.package",
	version = version,
	
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	
	author = author.name,
	author_email = author.email,
	
	license = 'MIT',
	keywords = (
			'entry point',
			'plugin',
			'extensions',
			'plugin manager',
			'plugin system',
			'canonicalization',
			'reference parsing'
		),
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = ['marrow.package'],
	include_package_data = True,
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	
	install_requires = [],
	
	extras_require = dict(
			development = tests_require + ['pre-commit'],  # Development-time dependencies.
		),
	
	tests_require = tests_require,
	
	zip_safe = False,
)
