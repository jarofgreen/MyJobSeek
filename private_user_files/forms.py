from django import forms
from datetime import datetime
import settings

class NewFileForm(forms.Form):
	File = forms.FileField()
	Note = forms.CharField(widget=forms.Textarea,required=False)
	def clean_File(self):
		"""Check Size is below allowed."""
		allowed_size = getattr(settings, "PRIVATE_USER_FILES_MAX_SIZE_INDIVIDUAL_FILE", 100)
		if self.cleaned_data['File'].size > allowed_size:
			raise forms.ValidationError("This file is to big; it is %s bytes and the maximum allowed is %s" % (self.cleaned_data['File'].size,allowed_size))
		return self.cleaned_data['File']










