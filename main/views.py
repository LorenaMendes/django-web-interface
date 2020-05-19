from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CrawlRequestForm, RawCrawlRequestForm
from .models import CrawlRequest

def home(response):
    return render(response, "main/home.html", {})

def monitoring(response):
    return render(response, "main/monitoring.html", {})

def create_crawl(response):
    if response.method == "POST":
        my_form = RawCrawlRequestForm(response.POST)
        
        if my_form.is_valid():
            # now the data is good
            new_crawl = CrawlRequestForm(my_form.cleaned_data)
            new_crawl.save()
            
    
    else:
        my_form = RawCrawlRequestForm()
    context = {
        'form' : my_form
    }
    return render(response, "main/create_crawl.html", context)