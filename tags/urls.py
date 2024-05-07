# Import the path function from Django's urls module, which is used for routing URLs to the appropriate view functions.
from django.urls import path
from . import views

# Define the URL patterns for the album app
urlpatterns = [
    path('my_tags/<int:tag_id>/', views.my_tags, name='my_tags'),
    path('all_tags/<int:tag_id>/', views.all_tags, name='all_tags'),
    path('most_popular/', views.most_popular, name='most_popular'),
]