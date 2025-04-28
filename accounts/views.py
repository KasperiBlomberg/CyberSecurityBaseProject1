from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        query = f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'"
        # This allows SQL injection, use this instead
        # user = authenticate(request, username=username, password=password)
        cursor = connection.cursor()
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return HttpResponse(f"Hello, {username}")
        else:
            return HttpResponse("Invalid credentials")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            user = User.objects.create(username=username, password=password)
            # The password is not hashed, use this instead
            # user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, "register.html")



def home_view(request):
    return render(request, "home.html")
