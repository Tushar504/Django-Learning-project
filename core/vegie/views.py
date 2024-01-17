from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def receipes(request):
    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        Receipe.objects.create(
            user=request.user,
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image)

        return redirect('/receipes')

    receipes = Receipe.objects.all()
    print(receipes[1].user)
    search = request.GET.get("search")
    if search:
        receipes = receipes.filter(receipe_name__icontains=search)
    else:
        search = ""

    return render(request, 'receipes.html', context={"receipes": receipes, "search": search})


@login_required(login_url='/login')
def update_receipe(request, id):
    receipe = Receipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        receipe.receipe_name = receipe_name
        receipe.receipe_description = receipe_description

        if receipe_image:
            receipe_image = receipe_image

        receipe.save()
        return redirect('/receipes')

    return render(request, "update_receipes.html", context={"receipe": receipe})


@login_required(login_url='/login')
def delete_receipe(request, id):
    receipe = Receipe.objects.get(id=id)
    receipe.delete()
    return redirect('/receipes')


def register(request):

    if request.method == "POST":
        data = request.POST

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username)

        user.set_password(password)
        user.save()

        messages.info(request, "User Registerd")
        return redirect("/login")

    return render(request, "register.html")


def login_page(request):

    if request.user.is_authenticated:
        return redirect("/receipes")

    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username)

        if not user.exists():
            messages.info(request, "Invalid Username")
            return redirect("/login")

        user = authenticate(username=username, password=password)

        if not user:
            messages.info(request, "Invalid Password")
            return redirect("/login")
        else:
            login(request, user=user)
            return redirect("/receipes")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login")
