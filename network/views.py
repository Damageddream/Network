import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, New_post



def index(request):
    posts = list(reversed(New_post.objects.all()))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "page_number": page_number
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
    posts = list(reversed(New_post.objects.all().filter(poster=profile.id)))
    user = User.objects.get(id=request.user.id)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
        "page_obj": page_obj,
        "page_number": page_number
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
        "page_obj": page_obj,
        "page_number": page_number
    })

@csrf_exempt
def edit(request,page,where):

    if where == "following":
        user = request.user
        posts_id = []
        for id in user.following.all():
            posts_id.append(id.id)
        posts = list(reversed(New_post.objects.all().filter(poster__in=posts_id)))      
    else:
        posts = list(reversed(New_post.objects.all()))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return JsonResponse([post.serialize() for post in page_obj], safe=False)

@csrf_exempt
def edit_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)
    try:
        post = New_post.objects.get(pk=post_id)
    except New_post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "PUT" and post.poster == request.user:
        print("posting")
        data = json.loads(request.body)
        text = data.get("text", "")
        post.post = text
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like(request, post_id):
    try:
        post = New_post.objects.get(pk=post_id)
    except New_post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
        
    print(request.user.id, post.u_likes, post.post)
    if request.method == "PUT":
        if request.user in post.u_likes.all():
            post.u_likes.remove(request.user)
            post.likes = len(post.u_likes.all())
            post.save()
        else:
            post.u_likes.add(request.user)
            post.likes = len(post.u_likes.all())
            post.save()
        return JsonResponse(post.serialize(), safe=False)