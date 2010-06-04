from django.db import models
from django.contrib.auth.models import User


class UserFile(models.Model):
	User = models.ForeignKey(User, related_name="fileuser")
	FileName = models.CharField(max_length=255)
	Size = models.PositiveIntegerField()
	ContentType = models.CharField(max_length=255, blank=True, null=True)
	CharSet = models.CharField(max_length=255, blank=True, null=True)
	Note = models.TextField(blank=True)
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)



	
