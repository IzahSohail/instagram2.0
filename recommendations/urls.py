from django.urls import path
from . import views as recommendations_views

urlpatterns = [
    path('you_may_also_know/', recommendations_views.friend_recommendations, name='you-may-also-know'),
    path('you_may_also_like/', recommendations_views.photo_recommendation, name ='you-may-also-like'),
]