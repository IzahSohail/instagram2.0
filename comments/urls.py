# Import the path function from Django's urls module, which is used for routing URLs to the appropriate view functions.
from django.urls import path

# Import the views module from the current package
from . import views

# Define the URL patterns for the album app
urlpatterns = [
    # The path to the create_album view function
    path('add_comment_to_photo/<int:photo_id>/', views.add_comment_to_photo, name='add_comment_to_photo'),
]

