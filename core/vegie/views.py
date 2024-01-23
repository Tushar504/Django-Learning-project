from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def receipes(request):
    receipes = Receipe.objects.all()
    search = request.GET.get("search")
    if search:
        receipes = receipes.filter(Q(receipe_name__icontains=search) | Q(receipe_description__icontains=search))
    else:
        search = ""

    return render(request, 'receipes.html', context={"receipes": receipes, "search": search})


@login_required(login_url='/login')
def add_receipe(request):
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

        return redirect('/')

    return render(request, 'add_receipe.html') 


@login_required(login_url='/login')
def view_receipe(request, id):
    receipe = Receipe.objects.get(id=id)

    return render(request, "view_receipe.html", context={"receipe": receipe})



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
        return redirect('/')

    return render(request, "update_receipes.html", context={"receipe": receipe})


@login_required(login_url='/login')
def delete_receipe(request, id):
    receipe = Receipe.objects.get(id=id)
    receipe.delete()
    return redirect('/')


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
        return redirect("/")

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
            next = request.GET.get("next")
            if next:
                return redirect(next)
            return redirect("/")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login")

