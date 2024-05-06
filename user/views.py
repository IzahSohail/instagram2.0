# Import Django utilities for rendering templates and redirecting URLs
from django.shortcuts import render, redirect, get_object_or_404
# Import the decorator to exempt a view from CSRF verification
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib import messages
# Import the form and model related to user registration
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from album.models import Album, Photo
from friends.models import Friends
from comments.models import Comment
# Import base64 for encoding and the Python Imaging Library (PIL) for image processing
import base64
from PIL import Image
from io import BytesIO
from django.contrib.auth.views import LoginView
#from django.contrib import messages

# Decorator to make this view exempt from CSRF token requirement
@csrf_exempt
def register(request):
    # Handle form submission
    if request.method == 'POST':
        # Initialize the form instance with data from the request
        form = UserRegistrationForm(request.POST, request.FILES)
        # Check if the form data is valid
        if form.is_valid():
            # Save the form data to a User model instance without committing to the database
            user = form.save(commit=False)
            user.username = user.first_name
            # Check if a photo was uploaded
            if 'photo' in request.FILES:
                # Open the uploaded image file with PIL
                image = Image.open(request.FILES['photo'])
                # Resize the image to a fixed size (e.g., 300x300 pixels) for consistency
                image = image.resize((300, 300), Image.LANCZOS)

                # Save the resized image to a buffer instead of a file
                buffer = BytesIO()
                image.save(buffer, format='JPEG')  # Adjust the format as needed
                buffer.seek(0)

                # Store the image data from the buffer to the user's photo field as binary data
                user.photo = buffer.read()

                # Encode the photo data in base64 for embedding in HTML
                photo_data = base64.b64encode(user.photo).decode('utf-8')
                user.save()  # Commit the user instance to the database

                # Render a template showing user info including the photo
                return render(request, 'user/user_info.html', {
                    'user': user,
                    'photo_data': photo_data,
                })
            else:
                # If no photo was uploaded, save and render the user info without a photo
                user.save()
                return render(request, 'user/user_info.html', {
                    'user': user,
                    'photo_data': None,
                })
    else:
        # If not a POST request, simply display the registration form
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Fetch the user with the provided email

            if user.password == password:
                # User authentication successful
                request.session['user_id'] = user.id
                print("Logged in successfully", user.id)
                return render(request, 'user/welcome.html', {'success_message': 'Welcome back', 'user': user})
            else:
                form = UserLoginForm()
                # Password is incorrect
                messages.error(request, 'Invalid email or password.')
                return render(request, 'user/login.html', {'error_message': 'Invalid email or password.', 'form':form})
        except User.DoesNotExist:
            form = UserLoginForm()
            # No user with the provided email exists
            messages.error(request, 'User does not exist.')
            return render(request, 'user/login.html', {'error_message': 'User does not exist.', 'form':form})
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    #print(request.session['user_id'])
    return render(request, 'user/logout.html')

def welcome(request):
    context = {}
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = { 'user': user, 'success_message': 'Welcome back' }
    # Render the welcome page template
    return render(request, 'user/welcome.html', context)

def users(request):
    # Check if the user is logged in by checking for 'user_id' in session
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        # Exclude the logged-in user from the list
        users_data = User.objects.exclude(id=user_id)
    else:
        # If no user is logged in, simply display all users
        users_data = User.objects.all()

    # Prepare user data for display, including encoding photos if present
    users_list = []
    for user in users_data:
        # Check if photo exists and encode if present
        photo_data = user.photo if hasattr(user, 'photo') and user.photo else None
        encoded_photo = base64.b64encode(photo_data).decode('utf-8') if photo_data else None
        photo_src = f"data:image/*;base64,{encoded_photo}" if encoded_photo else None

        # Add user details to the list, including encoded photo data
        users_list.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'photo_src': photo_src
        })

    # Render the users template, passing in the list of users for display
    return render(request, 'user/users.html', {'users': users_list})

def user_info(request):
    # Fetch the user instance using the session data
    user = User.objects.get(id=request.session['user_id'])
    #get the user's friends
    friends = Friends.objects.filter( user_a = user )
    #get the album based on the user
    albums = Album.objects.filter(user=user)
    # Render the user info template, passing in the user instance and encoded photo data
    return render(request, 'user/user_info.html', {'user': user, 'albums': albums, 'friends': friends})

#define a view to browse another users profile
def other_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    albums = Album.objects.filter(user=user)

    # Implement additional logic as needed, such as fetching user-related data
    return render(request, 'user/other_user_profile.html', {'user': user, 'albums': albums})

#defining a view that allows users to see the top 10 users on the site
def top_ten_users(request):
   
    #raw SQL query to get the top 10 users
    raw_query = """ 
    SELECT U.id, (SELECT COUNT(*) FROM comments_comment as C WHERE C.user_id = U.id) + (SELECT COUNT(*) FROM album_photo as P, album_album as A WHERE A.album_id = P.album_id AND A.user_id = U.id) AS score
    FROM user_user as U
    ORDER BY score DESC
    LIMIT 10;

    """.format(request.session['user_id'])

    #execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        rows = cursor.fetchall()

    #process the results
    top_users = []
    for row in rows:
        user_id, score = row
        user = User.objects.get(id=user_id)
        top_user = {'user': user, 'score': score}
        top_users.append(top_user)

    return render(request, 'user/top_ten_users.html', {'top_users': top_users})




