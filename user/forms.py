# Import Django's forms framework and the User model from the current app's models
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

# Define a ModelForm for user registration
class UserRegistrationForm(forms.ModelForm):
    # Manually add a FileField for uploading a photo. The 'required=False' parameter
    # indicates that the photo field is optional, and users can submit the form
    # without uploading a photo.
    photo = forms.FileField(required=False)

    # The Meta class holds configuration for this ModelForm. It tells Django
    # which model the form is for and which fields should be included in the form.
    class Meta:
        # Specifies the model associated with this form
        model = User

        # List of fields to be included in the form. These fields will be rendered
        # using their default widgets, except for the 'password' field which is
        # explicitly specified below.
        # Note: 'photo' is handled manually above, so it's not included in this list.
        fields = ['first_name', 'last_name', 'email', 'password', 'date_of_birth', 'gender', 'hometown']

        # The widgets dictionary allows you to specify custom widgets for certain fields.
        # Here, the 'password' field uses the PasswordInput widget, which renders it
        # as a password input, obscuring the text entered by the user.
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserLoginForm(forms.ModelForm):
    # The Meta class holds configuration for this ModelForm. It tells Django
    # which model the form is for and which fields should be included in the form.
    class Meta:
        # Specifies the model associated with this form
        model = User

        # List of fields to be included in the form. These fields will be rendered
        # using their default widgets, except for the 'password' field which is
        # explicitly specified below.
        # Note: 'photo' is handled manually above, so it's not included in this list.
        fields = [ 'email', 'password']

        # The widgets dictionary allows you to specify custom widgets for certain fields.
        # Here, the 'password' field uses the PasswordInput widget, which renders it
        # as a password input, obscuring the text entered by the user.
        widgets = {
            'password': forms.PasswordInput(),
        }