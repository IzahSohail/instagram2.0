from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Subquery, Count
from django.db import connection
from user.models import User
from friends.models import Friends


@csrf_exempt
def friend_recommendations(request):
    raw_query = """
    WITH friends_of_user AS (
        SELECT   F.user_b_id
        FROM     FRIENDS_FRIENDS AS F
        WHERE    F.user_a_id = {}
    ),
    friends_of_friends AS (
        (SELECT   F.user_b_id
         FROM     FRIENDS_FRIENDS AS F
         WHERE    F.user_a_id IN (SELECT user_b_id FROM friends_of_user) AND F.user_b_id NOT IN (SELECT user_b_id FROM friends_of_user))
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












'''
    #getting user and his friendships
    user        = User.objects.get(id=request.session['user_id'])
    friendships = Friends.objects.filter( user_a = user )

    #getting the user's friends as user objects in a list called friends
    friends = []
    for i in friendships:
        friend = User.objects.get(id = i.user_b.id)
        friends.append(friend)
   
    to_recommend = []
    #for each friend
    for friend in friends:
        #get a queryset of their friends
        friends_of_friend = Friends.objects.filter( user_a = friend )
         
        #and exclude friends that the user already has| THIS IS WRONG, YOU ARE NOT SUPPOSED TO EXCLUDE ONLY USER BUT ALL USER'S FRIENDS!!
        friends_of_friend_filtered = friends_of_friend.exclude(user_b = user)

        #append that filtered query set to the list of friends we will ultimately recommend to the user
        to_recommend.append(friends_of_friend_filtered)

    friends_of_friends = to_recommend[0]
    #but first, join all friends of friends
    for i in to_recommend[1::]:
        friends_of_friends = friends_of_friends.union(i)
    
    #query to group by id with and add an attribute count to each element of the queryset 
    friends_of_friends = friends_of_friends.values('id').annotate(count=Count('id'))

    #now it's safe to remove duplicates, because in the attribute "count", the number of mutual friends is preserved
    friends_of_friends = friends_of_friends.distinct()

    #finally, just ordering from highest number of mutual friends to lowest
    friends_of_friends = friends_of_friends.order_by('-count')

    return render(request, 'friends/add.html', {'users': friends_of_friends})
'''