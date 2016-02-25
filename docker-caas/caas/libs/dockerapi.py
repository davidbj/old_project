from caas.libs import config
from docker import Client 

class DockerApi(object):
	def __init__(self):
	#	self.docker_url = config.Config().docker_url
		pass

	def __connDocker(self):
		'''Connection docker service.'''

		urlObj = config.Getconfig()
		urlObj.getConfig = 'docker_url'
		docker_url = urlObj.getConfig
		conn = Client(base_url = docker_url)
		return conn

	@property
	def getImages(self):
		'''Get docker service images.'''

		client = self.__connDocker()
		images = client.images()
		return images
