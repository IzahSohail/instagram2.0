from django import forms
from user.models import User
from django.contrib.auth.forms import AuthenticationForm

class FriendSearchForm(forms.ModelForm):
    class Meta:
        # Specifies the model associated with this form
        model = User
        fields = ['first_name', 'last_name']