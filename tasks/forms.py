from django import forms
from tasks.models import Property


class UploadForm(forms.Form):
    property = forms.ModelChoiceField(queryset=Property.objects.all())
    csv_file = forms.FileField()