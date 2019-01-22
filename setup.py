#!/usr/bin/env python3

from setuptools import setup
from sys import argv, version_info as python_version
from pathlib import Path


if python_version < (3, 5):
	raise SystemExit("Python 3.5 or later is required.")

here = Path.cwd()
exec((here / "marrow" / "package" / "release.py").read_text('utf-8'))

tests_require = ['pytest', 'pytest-cov', 'pytest-flakes', 'pytest-isort']


setup(
	name = "marrow.package",
	version = version,
	description = description,
	long_description = (here / 'README.rst').read_text('utf-8'),
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
			'reference parsing',
			'import resolver',
		),
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = ('marrow.package', ),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	zip_safe = False,
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(argv) else [],
	
	install_requires = [
			'typeguard <= 2.3',
			'typing; python_version < "3.5"',  # 
		],
	
	extras_require = dict(
			development = tests_require + ['pre-commit'],  # Development-time dependencies.
		),
	
	tests_require = tests_require,
	
	entry_points = {
			'marrow.package.sample': [
					'name = marrow.package:name',
					'load = marrow.package:load',
					'traverse = marrow.package:traverse',
				]
		}
)
