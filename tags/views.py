from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

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
        
        owner = photo.owner

        photos_data.append({
            'photo_id': photo.photo_id, 
            'photo_data': photo_src,
            'owner': owner,
            'caption': photo.caption,
            'total_likes': total_likes,
            'comments': comments,
            'tags': tags
        })
    
    tag = Tag.objects.get(tag_id=tag_id)
    return render(request, 'tags/all_tags.html', {'photos': photos_data, 'tag': tag})


def most_popular(request):
    raw_query = """
    SELECT          Map.tag_id, COUNT(Map.photo_id) AS Count
    FROM            tags_phototagmapping AS Map, tags_tag AS Tag
    WHERE           Map.tag_id = Tag.tag_id
    GROUP BY        Map.tag_id
    ORDER BY        Count DESC;"""

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        rows = cursor.fetchall()

    tags =[]
    for row in rows:
        tag_id = row[0]
        tag = Tag.objects.get(tag_id=tag_id)
        tags.append(tag)

    return render(request, 'tags/most_popular.html', {'tags': tags})


@csrf_exempt
def tag_search(request):

    if request.method != 'POST':
        return render(request, 'tags/search_input.html')

    elif request.method == 'POST':
        tags = request.POST.get('tags').split(' ')

        with connection.cursor() as cursor:
            cursor.execute("""
                            CREATE TEMPORARY TABLE SEARCHED_TAGS (
                            tag_id INTEGER PRIMARY KEY)
                                                            """)

            for tag in tags:   
                cursor.execute("""
                                INSERT INTO SEARCHED_TAGS
                                VALUES ((SELECT tag_id FROM tags_tag AS Tags WHERE Tags.description = '{}'))
                                """.format(tag))

            raw_query = """
            SELECT  Photos.photo_id
            FROM	ALBUM_PHOTO AS Photos
            WHERE	NOT EXISTS (
                               (SELECT	SEARCHED_TAGS.tag_id
                                FROM 	SEARCHED_TAGS)
                                EXCEPT
                               (SELECT	Mapping.tag_id
                                FROM	TAGS_PHOTOTAGMAPPING AS Mapping
                                WHERE	Photos.photo_id = Mapping.photo_id));
            """

            cursor.execute(raw_query)
            rows = cursor.fetchall()
            
            photos=[]
            for row in rows:
                photo_id = row[0]
                photo = Photo.objects.get(photo_id=photo_id)
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
                
                owner = photo.owner

                photos_data.append({
                    'photo_id': photo.photo_id, 
                    'photo_data': photo_src,
                    'owner': owner,
                    'caption': photo.caption,
                    'total_likes': total_likes,
                    'comments': comments,
                    'tags': tags
                })

        return render(request, 'tags/tag_search.html', {'photos': photos_data})