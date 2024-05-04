from django.urls import path
from . import views as friends_views

urlpatterns = [
    path('search-friends/', friends_views.search, name='search-friends'),
    path('search-friends/add/', friends_views.add, name='add-friends'),

]