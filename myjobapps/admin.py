__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

from django.contrib import admin
from models import *

admin.site.register(Note)
admin.site.register(Job)
admin.site.register(Company)
admin.site.register(Agency)
