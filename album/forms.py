from django import forms

class AlbumForm(forms.Form):
    name = forms.CharField(max_length=64)