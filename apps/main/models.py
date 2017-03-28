from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATE_REGEX = re.compile(r'^(\d{4}-\d{2}-\d{2})')
# Create your models here.
class UserManager(models.Manager):
    def register(self, user_name, name, email, passw, cpass, dob):
        print name, email, passw, cpass
        errors = []
        today = datetime.datetime.now()
        successes = []
        valid = True
        if len(dob) < 1:
            errors.append('please enter your Date of Birth')
            valid = False
        try:
            t_date_time = ('%s %s' % (dob, '12:00'))
            t_date_time = datetime.datetime.strptime(t_date_time, '%Y-%m-%d %H:%M')

        except ValueError:
            errors.append('Incorrent date format')
            valid = False
        try:
            if t_date_time > today:
                errors.append(' Enter a valid DOB. Like any day before today :(')
                valid = False
        except TypeError:
            errors.append('Reformat your date to match YYYY-MM-DD')
            valid = False

        if len(email) < 1:
            errors.append("An email must be provided.")
            valid = False

        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email provided.")
            valid = False

        if User.objects.filter(email=email).exists():
            errors.append("Email is already in use. Please log in or try another email.")
            valid = False

        if len(user_name) < 4:
            errors.append("User Name must be provided and be atleast three characters long.")
            valid = False

        if len(name) < 4:
            errors.append("Name must be provided and be atleast three characters long.")
            valid = False

        elif re.search(r'[0-9]', name):
            errors.append("Name cannot contain a number.")
            valid = False

        elif not name.isalpha():
            errors.append("Name can only have letters.")
            valid = False

        if len(passw) < 8:
            errors.append("Password must be 8 characters")
            valid = False

        if len(cpass) < 2:
            errors.append("Confirm password cannot be empty.")
            valid = False

        elif passw != cpass:
            errors.append("Passwords must match.")
            valid = False

        if valid:
            passw_enc = bcrypt.hashpw(passw.encode(), bcrypt.gensalt())
            data = {
            	'name': name,
                'email': email,
                'password': passw_enc
            }
            User.objects.create(**data)

            successes.append("Account successfully created. Please log in now.")
            return (valid, errors, successes)
        else:

            return (valid, errors, successes)

    def login(self, email, passw):
        if not email or not passw:
            return (False, "Both email and password fields are required to login.")

        if not User.objects.filter(email=email).exists():
            return(False, "Email does not exist.")

        data = User.objects.get(email=email)
        hashed = data.password.encode()

        if bcrypt.hashpw(passw.encode(), hashed) == hashed:
            return (True, "Successful login!", data)

        else:
            return (False, "Incorrect password or email. Please try again.")

    def addFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        Friend.objects.create(user_friend=user, second_friend=friend)
        Friend.objects.create(user_friend=friend, second_friend=user)

    def removeFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        friendship1 = Friend.objects.get(user_friend=user, second_friend=friend)
        friendship2 = Friend.objects.get(user_friend=friend, second_friend=user)
        friendship1.delete()
        friendship2.delete()

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Friend(models.Model):
    user_friend = models.ForeignKey(User, related_name='requester')
    second_friend = models.ForeignKey(User, related_name='accepter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()