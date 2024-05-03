from django.urls import path
from . import views as friends_views

urlpatterns = [
    path('friends/', friends_views.friends, name='friends'),
    path('friends/search/', friends_views.search, name='search-friends'),
    path('friends/add/', friends_views.add, name='add-friends'),

]