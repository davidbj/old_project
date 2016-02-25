from django.db import models

# Create your models here.

class Images(models.Model):


	images_id = models.CharField(max_length=100, default='')
	name = models.CharField(max_length=100, default='')
	version = models.CharField(max_length=40, default='')
	created = models.CharField(max_length=40, default='')
	virtual_size = models.CharField(max_length=20, default='')

	def __unicode__(self):
		return self.images_id

