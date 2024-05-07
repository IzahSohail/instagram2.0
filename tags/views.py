from django.shortcuts import render
from django.db import connection

from album.models import Album, Photo, Photo_likes
from .models import Tag, PhotoTagMapping
from user.models import User

from comments.forms import CommentForm
from comments.models import Comment

import base64
from PIL import Image
from io import BytesIO


def my_tags(request, tag_id):

    raw_query = """
    SELECT          Photo.photo_id
    FROM            TAGS_PHOTOTAGMAPPING AS photo_tag_mapping, ALBUM_ALBUM AS Album, ALBUM_PHOTO AS Photo
    WHERE           Album.user_id = {} AND photo_tag_mapping.tag_id = {} AND Photo.album_id = Album.album_id AND photo_tag_mapping.photo_id = Photo.photo_id;
    """.format(request.session['user_id'], tag_id)

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        rows = cursor.fetchall()
    
    photos=[]
    for row in rows:
        photo_id = row[0]
        photo = Photo.objects.get(photo_id = photo_id)
        photos.append(photo)

    photos_data = []
    for photo in photos:
        encoded_photo = base64.b64encode(photo.photo_data).decode('utf-8')
        photo_src = f"data:image/*;base64,{encoded_photo}"

        #tags for each photo
        tags=[]
        photo_tag_map = PhotoTagMapping.objects.filter(photo=photo)
        for mapping in photo_tag_map:
            tags.append(mapping.tag)

        #comments for each photo
        comments = Comment.objects.filter(photo=photo)

        # Count likes for each photo
        total_likes = Photo_likes.objects.filter(photo=photo).count()
        
        photos_data.append({
            'photo_id': photo.photo_id, 
            'photo_data': photo_src,
            'caption': photo.caption,
            'total_likes': total_likes,
            'comments': comments,
            'tags': tags
        })
    
    tag = Tag.objects.get(tag_id=tag_id)
    return render(request, 'tags/my_tags.html', {'photos': photos_data, 'tag': tag})


def all_tags(request, tag_id):

    raw_query = """
    SELECT          Photo.photo_id
    FROM            TAGS_PHOTOTAGMAPPING AS photo_tag_mapping, ALBUM_PHOTO AS Photo
    WHERE           photo_tag_mapping.tag_id = {} AND photo_tag_mapping.photo_id = Photo.photo_id;
    """.format(tag_id)

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        rows = cursor.fetchall()
    
    photos=[]
    for row in rows:
        photo_id = row[0]
        photo = Photo.objects.get(photo_id = photo_id)
        photos.append(photo)

    photos_data = []
    for photo in photos:
        encoded_photo = base64.b64encode(photo.photo_data).decode('utf-8')
        photo_src = f"data:image/*;base64,{encoded_photo}"

        #tags for each photo
        tags=[]
        photo_tag_map = PhotoTagMapping.objects.filter(photo=photo)
        for mapping in photo_tag_map:
            tags.append(mapping.tag)

        #comments for each photo
        comments = Comment.objects.filter(photo=photo)

        # Count likes for each photo
        total_likes = Photo_likes.objects.filter(photo=photo).count()
        
        photos_data.append({
            'photo_id': photo.photo_id, 
            'photo_data': photo_src,
            'caption': photo.caption,
            'total_likes': total_likes,
            'comments': comments,
            'tags': tags
        })
    
    tag = Tag.objects.get(tag_id=tag_id)
    return render(request, 'tags/all_tags.html', {'photos': photos_data, 'tag': tag})


