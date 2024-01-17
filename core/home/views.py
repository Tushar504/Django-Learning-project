from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    peoples = [
        {'name': 'vishvaraj dhanawade', 'age': 40},
        {'name': 'harshal ahire', 'age': 17},
        {'name': 'anamol soman', 'age': 25},
        {'name': 'tushar ahire', 'age': 26},
    ]

    return render(request, "index.html", context={"peoples": peoples})
