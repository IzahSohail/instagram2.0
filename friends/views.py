from django.shortcuts import render
from .models import Friends
from .forms import FriendSearchForm
from user.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def friends(request):
    user = User.objects.get(id=request.session['user_id'])
    friends = Friends.objects.filter( user_a = user )
    context = { 'friends': friends }
    return render(request, 'friends/friends.html', context)

@csrf_exempt
def search(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        users = User.objects.filter(first_name=first_name, last_name=last_name)
        if users.exists():
            return render(request, 'friends/add.html' , {'users': users})

        else:
            form = FriendSearchForm()
            return render(request, 'friends/search.html', {'error_message': 'User does not exist. Enter the correct name of your friend.', 'form':form})
    else:
        form = FriendSearchForm()
        return render(request, 'friends/search.html', {'form': form})

@csrf_exempt
def add(request):
    if request.method == 'POST':
        user   = User.objects.get(id=request.session['user_id'])
        friend = User.objects.get(id=request.POST.get('friend_id'))

        if Friends.objects.filter(user_a=user, user_b=friend).exists():
            form = FriendSearchForm()
            return render(request, 'friends/search.html', {'error_message': friend.first_name + " is already your friend!", 'form': form})

        else:
            friendship = Friends.objects.create(user_a = user, user_b = friend)
            return render(request, 'friends/success.html', {'friend': friend})
