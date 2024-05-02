from django import forms
from .models import Album, Photo


class createAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_name']
        widgets = {
            'album_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


