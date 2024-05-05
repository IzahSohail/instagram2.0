from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Album, Photo
from tags.models import Tag, PhotoTagMapping
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


        tags = request.POST.get('tags', '')
        tags_array = tags.split()  # Split the tags string based on whitespace and store the result in an array

        for tag_description in tags_array:                                      #for every tag in tags_array
            if not (Tag.objects.filter(description=tag_description).exists()):  #check if that tag already exists
                new_tag = Tag(description = tag_description)                    #if not, then make that tag
                new_tag.save()
                photo_tag_mapping = PhotoTagMapping(tag=new_tag, photo=photo)   #then make the photo-tag mapping
                photo_tag_mapping.save()
                continue
            tag = Tag.objects.get(description=tag_description)
            photo_tag_mapping = PhotoTagMapping(tag=tag, photo=photo)
            photo_tag_mapping.save()

        # Redirect to the same album view to see the uploaded photo
        return redirect('view_album', album_id=album_id)
    
    else:
        # Prepare photos data for display
        photos = Photo.objects.filter(album=album)
        photo_tag_maps=[]
        for photo in photos:
            encoded_photo = base64.b64encode(photo.photo_data).decode('utf-8')
            photo_src = f"data:image/*;base64,{encoded_photo}"
            photo.photo_data = photo_src

            #preparing them tags
            photo_tag_map = PhotoTagMapping.objects.filter(photo=photo)
            tags=[]
            for mapping in photo_tag_map:   #perhaps i did it in an unnecassarily complicated way
                tags.append(mapping.tag)    #but idk how else to extract tags, it's not that straightforward

            photo_tag_dict = {'photo': photo, 'tags': tags}
            photo_tag_maps.append(photo_tag_dict)

        return render(request, 'album/view_album.html', {'album': album, 'photo_tag_maps': photo_tag_maps})


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


def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, photo_id=photo_id)
    album_id = photo.album.album_id
    photo.delete()
    return redirect('view_album', album_id=album_id)

def delete_album(request, album_id):
    # Retrieve the album using the primary key 'id'
    album = get_object_or_404(Album, album_id=album_id)
    album.delete()
    # Redirect to the 'user_info' view assuming it's correctly defined in your urls.py
    return redirect('user_info')