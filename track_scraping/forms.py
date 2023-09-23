from django import forms

class ArtistForm(forms.Form):
    name = forms.CharField(label='name',max_length=100)