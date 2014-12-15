# encoding: utf-8

import os


class Mine(object):
	def canary(self):
		pass

if not hasattr(Mine.canary, 'im_class') and not hasattr(Mine.canary, '__qualname__'):
	os.environ['CANARY'] = "DEAD"
