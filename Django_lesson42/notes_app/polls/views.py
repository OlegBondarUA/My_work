from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello to the entire group studying Python, "
                        "you are the best and our teacher is awesome.")

# Create your views here.
