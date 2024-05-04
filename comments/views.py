from django.shortcuts import render, redirect
from .forms import CommentForm
from album.models import Photo
from user.models import User

# Create your views here.
def add_comment_to_photo(request, photo_id):
    photo = Photo.objects.get(photo_id=photo_id)
    album_id = photo.album.album_id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.comment_text = form.cleaned_data['comment_text']
        comment.photo_id = photo.photo_id
        comment.user = User.objects.get(id=request.session['user_id'])
        comment.save()
        #trigger browse_album view
        return redirect(f'/browse_album/{album_id}/')
    else:
        return redirect('/browse_album', {'album_id': album_id})
