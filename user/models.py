# Import the models module from Django's database library
from django.db import models


# Define the User model, which extends Django's Model class
class User(models.Model):
    # Define a character field for the user's first name with a maximum length of 50 characters
    first_name = models.CharField(max_length=50)

    # Define a character field for the user's last name, also with a maximum length of 50 characters
    last_name = models.CharField(max_length=50)

    # Define an email field for the user. The 'unique=True' argument ensures that each email in the database is unique
    email = models.EmailField(unique=True)

    # Define a character field for the user's password. In a real application, you'd likely
    # use Django's built-in User model or handle passwords more securely
    password = models.CharField(max_length=50)

    date_of_birth = models.DateField(null=True)

    gender = models.CharField(max_length=1, null=True)

    hometown = models.CharField(max_length=50, null=True)

    # Define a binary field for storing the user's photo. This field is intended to store
    # binary data (e.g., an image file), but consider using Django's ImageField or FileField
    # for handling file uploads in a more conventional way
    photo = models.BinaryField()

    # Define the __str__ method to return the user's email when printing an instance
    # of this model. This improves readability and debugging.
    def __str__(self):
        return self.email
