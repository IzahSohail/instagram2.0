# Import the path function from Django's urls module, which is used for routing URLs to the appropriate view functions.
from django.urls import path
# Import the views module from the current package (denoted by .) to reference view functions defined within it.
from . import views as user_views
from django.contrib.auth import views as auth_views

# Define the urlpatterns list, which Django uses to match browser requests to the correct view functions based on the URL path.
urlpatterns = [
    # Define a URL pattern for the root URL (''). This pattern routes requests to the welcome view function
    # defined in the views module. The name='welcome' argument assigns a name to this URL pattern,
    # allowing it to be referenced by this name elsewhere in your Django project.
    path('', user_views.welcome, name='welcome'),

    # Define a URL pattern for the '/register/' path. Requests to 'http://<your_domain>/register/'
    # are routed to the register view function. Naming this URL pattern 'register' allows for easy reference throughout the project.
    path('register/', user_views.register, name='register'),


    path('login/', user_views.login, name='login'),
    path('logout/', user_views.welcome, name='logout'),


    # Define a URL pattern for the '/users/' path. This pattern routes requests to the users view function,
    # which is expected to display a list of users. Like the others, this URL pattern is named ('users')
    # to facilitate referencing it by name in the project.
    path('users/', user_views.users, name='users'),
]
