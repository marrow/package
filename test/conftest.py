import os


class Mine:
	def canary(self):
		pass

if not hasattr(Mine.canary, 'im_class') and not hasattr(Mine.canary, '__qualname__'):
	os.environ['CANARY'] = "DEAD"
