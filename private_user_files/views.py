from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
#from django import forms
from django.template import RequestContext
import forms as forms
from models import *
from datetime import datetime
import os
import settings

@login_required
def listFiles(request):
	if request.method == 'POST':
		form = forms.NewFileForm(request.POST, request.FILES )
		if form.is_valid():
			cd = form.cleaned_data
			uf = UserFile(User=request.user, FileName=request.FILES['File'].name, Size=request.FILES['File'].size , ContentType=request.FILES['File'].content_type, CharSet=request.FILES['File'].charset, Note=cd['Note'])
			uf.save()

			folder = os.path.join(settings.PRIVATE_USER_FILES_LOCATION, str(uf.id % getattr(settings, "PRIVATE_USER_FILES_BUCKETS", 100)))
			os.makedirs(folder)

			destination = open(os.path.join(folder,str(uf.id)), 'wb+')
			for chunk in request.FILES['File'].chunks():
				destination.write(chunk)
			destination.close()

			return HttpResponseRedirect('/files/')
	else:
		form = forms.NewFileForm( )
	userfiles =  UserFile.objects.filter(User=request.user).order_by('FileName')
	return render_to_response('files.html',{ "userfiles":userfiles, 'form': form,}, context_instance=RequestContext(request))



