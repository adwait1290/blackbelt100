from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.core.urlresolvers import reverse
from .models import User, UserManager, Friend

# Create your views here.
def index(request):

    return render(request, 'main/index.html')

def register(request):
	if request.method == 'POST':
		post = request.POST
		data = {
			'name': post['name'],
			'user_name':post['user_name'],
			'email': post['email'],
			'passw': post['pass'],
			'cpass': post['cpass'],
			'dob': post['dob'],
		}

		response = User.objects.register(**data)
		# errorMsg = response[1]
		# for x in range(len(errorMsg)):
		# 	messages.add_message(request,messages.ERROR, errorMsg[x])
		for i in response[1]:
			messages.error(request, i)
		for i in response[2]:
			messages.success(request, i)
		print response[1]
		return redirect('/')

def login(request):
	if request.method == 'POST':
		data = {
			'email': request.POST['email'],
			'passw': request.POST['pass'],
		}

		response = User.objects.login(**data)

		if response[0]:
			messages.success(request, response[1])
			request.session['user_id'] = response[2].id
			request.session['user_name'] = response[2].name
		else:
			messages.error(request, response[1])
			return redirect('/')
		return redirect(reverse('main:friends'))

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')
        request.session.pop('user_name')
        messages.success(request, "You have successfully logged out!")

    return redirect('/')

def friends(request):
    me = User.objects.get(id=request.session['user_id'])
    try:
        users = User.objects.all()
        others = []
        for other_user in users:
            if (other_user.id != request.session['user_id']):
                others.append(other_user)
            else: 
                users = None
    except:
        users = None

    try:
        friends = Friend.objects.filter(user_friend=me)
        real_friends = []
        for each_friend in friends:
            real_friends.append(each_friend.second_friend)
            friends = real_friends
        real_others = []
        for other_user in others:
            if (other_user not in real_friends):
                real_others.append(other_user)
                users = real_others
    except:
        friends = None

    context = {
        'me' : me,
        'users' : users,
        'friends' : friends
    }
    return render(request, 'main/friends.html', context)

def profile(request, id):
    profile = User.objects.get(id=id)
    context = {
        'user' : profile
    }
    return render(request, 'main/profile.html', context)

def add_friend(request, id):
    User.objects.addFriend(request.session['user_id'], id)
    return redirect('/friends')

def remove_friend(request, id):
    User.objects.removeFriend(request.session['user_id'], id)
    return redirect('/friends')