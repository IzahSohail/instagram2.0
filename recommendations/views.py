from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Subquery, Count
from django.db import connection
from user.models import User
from friends.models import Friends
from album.models import Album, Photo, Photo_likes
from tags.models import Tag, PhotoTagMapping
from comments.forms import CommentForm
from comments.models import Comment

import base64
from PIL import Image
from io import BytesIO


@csrf_exempt
def friend_recommendations(request):
    raw_query = """
    WITH friends_of_user AS (
        SELECT   F.user_b_id
        FROM     FRIENDS_FRIENDS AS F
        WHERE    F.user_a_id = {}
    ),
    friends_of_friends AS (
         SELECT   F.user_b_id
         FROM     FRIENDS_FRIENDS AS F
         WHERE    F.user_a_id IN (SELECT user_b_id FROM friends_of_user) AND F.user_b_id NOT IN ((SELECT user_b_id FROM friends_of_user) UNION SELECT {} AS user_b_id)
    )
    SELECT          B.user_b_id, COUNT(B.user_b_id) AS mutual_friends
    FROM            friends_of_friends AS B
    GROUP BY        B.user_b_id
    ORDER BY        COUNT(B.user_b_id) DESC;
    """.format(request.session['user_id'], request.session['user_id'])

    #execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        rows = cursor.fetchall()

    #process the results
    recommendations = []
    for row in rows:
        recommended_used_id, mutual_friends_count = row
        recommended_user = User.objects.get(id=recommended_used_id)
        friend_recommendation = {'user': recommended_user, 'mutual_friends_count': mutual_friends_count}
        recommendations.append(friend_recommendation)

    return render(request, 'recommendations/friend_rec.html', {'recommendations': recommendations})

def photo_recommendation(request):
    
    raw_query = """
                  WITH Auxi AS (SELECT  Mapping2.photo_id, Mapping2.tag_id
                    FROM    tags_phototagmapping AS Mapping2, album_photo AS Photos2
                    WHERE   Mapping2.photo_id = Photos2.photo_id AND Mapping2.tag_id IN (SELECT	Mapping.tag_id
                                                                                         FROM	album_photo AS Photos, tags_phototagmapping AS Mapping
                                                                                         WHERE	Photos.owner_id = {} AND Photos.photo_id = Mapping.photo_id	
                                                                                         GROUP BY  Mapping.tag_id
                                                                                         ORDER BY  COUNT(Mapping.photo_id) DESC
                                                                                         LIMIT 5)
                                    
                    EXCEPT
                    (SELECT  Photos3.photo_id, Mapping3.tag_id
                     FROM    album_photo AS Photos3, tags_phototagmapping as Mapping3 
                     WHERE   Photos3.owner_id = {} AND Mapping3.photo_id = Photos3.photo_id))

                    SELECT Auxi.photo_id
                    FROM Auxi
                    GROUP BY Auxi.photo_id
                    ORDER BY    COUNT(Auxi.tag_id) DESC, (SELECT    COUNT(Mapping5.tag_id)
                                                          FROM      tags_phototagmapping as Mapping5
                                                          WHERE     Mapping5.photo_id = Auxi.photo_id
                                                              GROUP BY  Mapping5.photo_id);

                    
                """.format(request.session['user_id'], request.session['user_id'])


    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        rows = cursor.fetchall()

    recommendations = []
    for row in rows:
        photo_id = row[0]
        photo = Photo.objects.get(photo_id=photo_id)
        recommendations.append(photo)
    
    photos_data = []
    for photo in recommendations:
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
            'caption': photo.caption,
            'total_likes': total_likes,
            'owner': owner,
            'comments': comments,
            'tags': tags
        })

    return render(request, 'recommendations/photo_rec.html', {'photos': photos_data})
