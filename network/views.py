import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator


from .models import User, New_post



def index(request):
    posts = list(reversed(New_post.objects.all()))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def new_post(request):
    if request.method == "POST":
        post_text = request.POST["post_text"]
        author = request.user
        post = New_post(poster=request.user, post=post_text)
        post.save()
        return render(request, "network/new_post.html", {
            "post_text": post_text,
            "author": author
        })
    else:
        return render(request, "network/new_post.html")

def profile(request, user_id):
    profile = User.objects.get(id=user_id)
    posts = reversed(New_post.objects.all().filter(poster=profile.id))
    user = User.objects.get(id=request.user.id)


    if request.method == "POST":
        if "follow" in request.POST:
            profile.followers.add(user.id)
            profile.followers_number = len(profile.followers.all())
            profile.save()
            user.following.add(profile.id)
            user.following_number = len(user.following.all())
            user.save()
        elif "unfollow" in request.POST:
            profile.followers.remove(user.id)
            profile.followers_number = len(profile.followers.all())
            profile.save()
            user.following.remove(profile.id)
            user.following_number = len(user.following.all())
            user.save()


    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": posts
    })

def following(request):
    user = request.user
    posts_id = []
    for id in user.following.all():
        posts_id.append(id.id)
    posts = list(reversed(New_post.objects.all().filter(poster__in=posts_id)))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

def edit(request):
    posts = list(reversed(New_post.objects.all()))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return JsonResponse([post.serialize() for post in page_obj], safe=False)
    
def edit_post(request, post_id):
    try:
        post = New_post.objects.get(pk=post_id)
    except New_post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(post.serialize())
