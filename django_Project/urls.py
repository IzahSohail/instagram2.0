from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Site URLs
    # This line includes all the URLs for the admin site.
    # The Django admin site is a powerful feature that provides a web interface for managing your site’s data.
    # By visiting /admin/ on your site, you can add, edit, and delete objects.
    path('admin/', admin.site.urls),

    # Include register app URLs
    # The include function allows referencing other URLconfs.
    # Here it's used to include URLs from the 'register' application.
    # This means that every URL under the 'register' app will be accessible from the root of the site.
    # For example, if 'register' has a URL pattern named 'profile', it will be accessible as '/profile/'.
    path('', include('user.urls')),
    path('user_info/', include('album.urls')),
    path('user_info/', include('friends.urls')),
]
