from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import Post
import re


def is_at_least_decent_password(password):
    """This is function copied from internet"""
    # Check if password is at least 8 characters long
    if len(password) < 8:
        return False
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    # Check for at least one special character
    if not re.search(r'[\W_]', password):  # Non-word character (e.g. !, @, #)
        return False
    return True

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        query = f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'"
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        # This allows SQL injection, use this instead
        # user = authenticate(request, username=username, password=password)

        if row:
            user = User.objects.get(username=username)
            login(request, user)  # actually log the user in
            return redirect("home")
        else:
            return HttpResponse("Invalid credentials")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            # if not is_at_least_decent_password(password):
            #     messages.error(request, "Password must be at least 8 characters long, contain a digit, an uppercase letter, and a special character.")
            #     return render(request, "register.html")
            user = User.objects.create(username=username, password=password)
            # The password is not hashed, use this instead
            # user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "register.html")

# Delete the @csrf_exempt to fix
@csrf_exempt
def home_view(request):
    if request.method == "POST":
        content = request.POST.get("content")
        Post.objects.create(content=content)
        return redirect("home")

    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})
