#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from caas.libs import dockerapi
from caas.libs.formattime import FormatTime
from caas.apps.caas.models import Images

# Create your views here.


def login(req):
	'''Login caas system.'''
	pass

def images(req):
	'''images configure.'''

	imgs_ld = []
	images_obj = dockerapi.DockerApi()
	imgs = images_obj.getImages
	#return HttpResponse(images)
	for image in imgs:
		img_dc={}
		imageName = image.get('RepoTags')[0].split(':')[0]
		imageVersion = image.get('RepoTags')[0].split(':')[1]
		created = FormatTime.localtimeToFormattime(image.get('Created'))

		img_dc['id'] = image.get('Id')
		img_dc['name'] = imageName
		img_dc['version'] = imageVersion
		img_dc['created'] = created
		img_dc['VirtualSize'] = str(image.get('VirtualSize')/1000/1000)+" MB"
        
		imgs_ld.append(img_dc)

		if not Images.objects.filter(images_id=image.get('Id')):
			orm_img = Images()
			orm_img.images_id = image.get('Id')
			orm_img.name = imageName
			orm_img.version = imageVersion
			orm_img.created = created
			orm_img.VirtualSize = str(image.get('VirtualSize')/1000/1000)+"MB"
			orm_img.save()
    
	return render(req, 'images.html', {'imagesData': imgs_ld})

def container(req):
	'''Container configure.'''

	return render(req, 'tables.html')

def form_container(req):
	'''add container and editor container.'''
	return render(req, 'forms.html')
