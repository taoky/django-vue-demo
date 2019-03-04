from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from demo.response import response as resp


# About user auth: https://docs.djangoproject.com/en/2.1/topics/auth/
@require_POST
def register(request):
    username = request.POST["username"]
    password = request.POST["password"]

    if User.objects.filter(username=username).exists():
        # We don't want a same user register twice!
        return resp(1)
        # FIXME: using magic number here is NOT a good idea, any better way?

    user = User.objects.create_user(username=username, password=password)
    user.save() # save to database
    return resp()


@require_POST
def login(request):
    if request.user.is_authenticated:
        return resp(2)

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return resp() # success
    else:
        return resp(3)
