# forms.py
from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()
    # Add other fields if needed
