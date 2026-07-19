from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ProfileForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    posts = request.user.post_set.all().order_by("-created_at")

    return render(request, "profile.html", {
        "profile": profile,
        "posts": posts,
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})
