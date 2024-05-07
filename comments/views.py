from django.shortcuts import render, redirect
from .forms import CommentForm
from album.models import Photo
from user.models import User
from .models import Comment
from django.db import connection 


# Create your views here.
def add_comment_to_photo(request, photo_id):
    photo = Photo.objects.get(photo_id=photo_id)
    album_id = photo.album.album_id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.comment_text = form.cleaned_data['comment_text']
        comment.photo_id = photo.photo_id
        if 'user_id' in request.session:
            comment.user = User.objects.get(id=request.session['user_id'])
        else: #set user to null if not logged in
            comment.user = None
        comment.save()
        #trigger browse_album view
        return redirect(f'/browse_album/{album_id}/')
    else:
        return redirect('/browse_album', {'album_id': album_id})
    
def comments_search(request):
    # Initialize an empty list for comments if no search is made
    users_with_comments = []

    if request.method == 'POST':
        search_text = request.POST.get('search_text', '')
        # Raw SQL query adjusted to include parameterized input
        raw_query = """
        SELECT 
            U.id, U.first_name, U.last_name,
            COUNT(*) AS matching_comments_count
        FROM 
            user_user AS U, comments_comment AS C
        WHERE 
            C.comment_text LIKE %s AND U.id = C.user_id
        GROUP BY 
            U.id, U.first_name, U.last_name
        ORDER BY 
            matching_comments_count DESC;
        """

        with connection.cursor() as cursor:
            # Execute the query with parameterization to prevent SQL injection
            cursor.execute(raw_query, [f'%{search_text}%'])
            rows = cursor.fetchall()

        # Convert the rows into a more friendly format
        users_with_comments = [
            {'user_id': row[0], 'first_name': row[1], 'last_name': row[2], 'comment_count': row[3]}
            for row in rows
        ]

    # Render results whether there was a post request or not
    return render(request, 'comments/comments_search.html', {'users_with_comments': users_with_comments})
