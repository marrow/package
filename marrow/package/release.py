"""Release information."""

from collections import namedtuple


class VersionInfo(namedtuple('VersionInfo', ('major', 'minor', 'micro', 'releaselevel', 'serial'))):
	major:int
	minor:int
	micro:int
	releaselevel:str
	serial:int
	
	def __str__(self):
		main = f"{self.major}.{self.minor}.{self.micro}"
		supplement = f"{self.releaselevel[0]}{self.serial}"
		return main if self.releaselevel == 'final' else (main + supplement)


class Author(namedtuple('Author', ('name', 'email'))):
	name:str
	email:str


version_info = VersionInfo(2, 1, 0, 'final', 1)
version = str(version_info)

author = Author("Alice Bevan-McGregor", 'alice@gothcandy.com')

description = "A collection of utilities for resolving object names, names to objects, and managing plugins/extensions."
url = 'https://github.com/marrow/package/'
