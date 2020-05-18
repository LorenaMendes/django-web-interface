from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def home(response):
    return render(response, "main/home.html", {})

def crawlers(response):
    return render(response, "main/crawlers.html", {})

def monitoring(response):
    return render(response, "main/monitoring.html", {})