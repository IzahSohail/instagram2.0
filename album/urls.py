# Import the path function from Django's urls module, which is used for routing URLs to the appropriate view functions.
from django.urls import path

# Import the views module from the current package
from . import views

# Define the URL patterns for the album app
urlpatterns = [
    # The path to the create_album view function
    path('create_album/', views.create_album, name='create_album'),
    # The path to the view_album view function, which takes an album_id as an argument
    path('view_album/<int:album_id>/', views.view_album, name='view_album'),
    path('browse_album/<int:album_id>/', views.browse_album, name='browse_album'),
    path('delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('delete_album/<int:album_id>/', views.delete_album, name='delete_album'),
]