from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth  # avoid login, logout name conflicting
from django.core import serializers

from demo.response import response as resp
from demo.models import Note
import json


# About user auth: https://docs.djangoproject.com/en/2.1/topics/auth/
@csrf_exempt
def register(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req["username"]
        password = req["password"]

        if User.objects.filter(username=username).exists():
            # We don't want a same user register twice!
            return resp(1)

        user = User.objects.create_user(username=username, password=password)
        user.save()  # save to database
        return resp()
    else:
        return render(request, 'signUp.html')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']

        user = authenticate(username=username, password=password)

        if request.user.is_authenticated and request.user.id == user.id:
            auth.logout(request)

        if user is not None:
            auth.login(request, user)
            return resp()  # success
        else:
            return resp(3)
    else:
        return render(request, 'signIn.html')


@require_POST
@csrf_exempt
def logout(request):
    if not request.user.is_authenticated:
        return resp(4)

    auth.logout(request)
    return resp()


@require_GET
def get_notes(request):
    if not request.user.is_authenticated:
        return resp(4)

    notes = Note.objects.filter(user=request.user).all()
    # https://docs.djangoproject.com/en/2.1/topics/serialization/#serialization-formats-json
    notes = json.loads(serializers.serialize("json", notes, fields=("content", "add_date")))
    notes = [i["fields"] for i in sorted(notes, key=lambda k: k["pk"])]
    return resp(items=notes, username=request.user.username)


@require_POST
@csrf_exempt
def add_notes(request):
    if not request.user.is_authenticated:
        return resp(4)

    req = json.loads(request.body)
    content = req["content"]

    note = Note.objects.create(content=content, user=request.user)
    note.save()
    return resp(add_date=note.add_date)


@login_required(login_url="/login")
def index(request):
    return render(request, 'user.html')
