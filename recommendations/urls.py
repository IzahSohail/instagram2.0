from django.urls import path
from . import views as recommendations_views

urlpatterns = [
    path('you_may_also_know', recommendations_views.friend_recommendations, name='you-may-also-know'),
]