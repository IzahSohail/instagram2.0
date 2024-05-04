from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Album, Photo
from user.models import User

from .forms import createAlbumForm
from comments.forms import CommentForm
from comments.models import Comment

import base64
from PIL import Image
from io import BytesIO


def create_album(request):
    if request.method == 'POST':
        form = createAlbumForm(request.POST)
        if form.is_valid():
            
            album = form.save(commit=False)
            user = User.objects.get(id=request.session['user_id'])
            album.user = user
            album.save()
            return redirect('view_album', album_id=album.album_id)
    else:
        form = createAlbumForm()
    return render(request, 'album/create_album.html', {'form': form})


def view_album(request, album_id):
    album = get_object_or_404(Album, album_id=album_id)

    if request.method == 'POST' and 'photo' in request.FILES:
        photo_file = request.FILES['photo']

        # Open the uploaded image file with PIL
        image = Image.open(photo_file)

        # Resize the image to a fixed size (e.g., 300x300 pixels) for consistency
        image = image.resize((300, 300), Image.LANCZOS)

        # Save the resized image to a buffer instead of a file
        buffer = BytesIO()
        image.save(buffer, format='JPEG')  # Adjust the format as needed
        buffer.seek(0)

        # Store the image data from the buffer to the photo's photo_data field as binary data
        photo_data = buffer.read()

        # Create a new Photo instance
        caption = request.POST.get('caption', '')
        photo = Photo(photo_data=photo_data, caption=caption, album=album)
        photo.save()

        # Redirect to the same album view to see the uploaded photo
        return redirect('view_album', album_id=album_id)
    
    else:
        # Prepare photos data for display
        photos = Photo.objects.filter(album=album)

        for photo in photos:
            encoded_photo = base64.b64encode(photo.photo_data).decode('utf-8')
            photo_src = f"data:image/*;base64,{encoded_photo}"
            photo.photo_data = photo_src


        return render(request, 'album/view_album.html', {'album': album, 'photos': photos})


#define a view for other people to browse through your albums but not add to it
def browse_album(request, album_id):
    
    album = get_object_or_404(Album, album_id=album_id)
    photos = Photo.objects.filter(album=album)
    comments = Comment.objects.all()

    for photo in photos:
        encoded_photo = base64.b64encode(photo.photo_data).decode('utf-8')
        photo_src = f"data:image/*;base64,{encoded_photo}"
        photo.photo_data = photo_src


    return render(request, 'album/browse_album.html', {'album': album, 'photos': photos, 'comments': comments , 'form': CommentForm()})