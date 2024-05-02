from django.shortcuts import render

# Create your views here.
from .models import Album, Photo
from user.models import User

from .forms import createAlbumForm


def create_album(request):
    if request.method == 'POST':
        form = createAlbumForm(request.POST)
        if form.is_valid():
            
            album = form.save(commit=False)
            user = User.objects.get(id=request.session['user_id'])
            album.user = user
            album.save()
            return render(request, 'album/view_album.html', {'album': album})
    else:
        form = createAlbumForm()
    return render(request, 'album/create_album.html', {'form': form})

def view_album(request, album_id):

    if request.method == 'POST':
        album = Album.objects.get(album_id=album_id)
        caption = request.POST.get('caption')
        photo = Photo(album=album, caption=caption)
        photo.save()
        photos = Photo.objects.filter(album=album)
        return render(request, 'album/view_album.html', {'album': album, 'photos': photos})
    
    else: 
        album = Album.objects.get(album_id=album_id)
        photos = Photo.objects.filter(album=album)
        return render(request, 'album/view_album.html', {'album': album, 'photos': photos})


