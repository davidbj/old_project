#-*- coding:utf-8 -*-


#def getData():
#	return {
#		'docker_url':'tcp://172.16.10.204:2376',
#	}


class Getconfig(object):
	def __init__(self):
		pass

	def setConfig(self):
		'''公共配置'''
		return {
			'docker_url': 'tcp://172.16.10.204:2376',
		}

	@property
	def getConfig(self):
		return self._getConfig

	@getConfig.setter
	def getConfig(self, key):

		self._getConfig = self.setConfig()[key]

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r'key Error.')

