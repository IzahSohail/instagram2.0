# Import the path function from Django's urls module, which is used for routing URLs to the appropriate view functions.
from django.urls import path

# Import the views module from the current package
from . import views

# Define the URL patterns for the album app
urlpatterns = [
    path('my_tags/' , views.my_tags, name='my_tags'),
]