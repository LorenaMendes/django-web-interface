from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CrawlRequestForm, RawCrawlRequestForm
from .models import CrawlRequest

def home(response):
    return render(response, "main/home.html", {})

def monitoring(response):
    return render(response, "main/monitoring.html", {})

def create_crawl(response):
    context = {}
    if response.method == "POST":
        my_form = RawCrawlRequestForm(response.POST)
        
        if my_form.is_valid():
            print(response.POST)

            new_crawl = CrawlRequestForm(my_form.cleaned_data)
            new_crawl.save()

            objs = CrawlRequest.objects
            my_obj = objs.filter(base_url = my_form.cleaned_data['base_url'])
            
            context['url'] = my_form.cleaned_data['base_url']
            context['id'] = my_obj.last().id
            
            return render(response, "main/steps_creation.html", context)
    else:
        my_form = RawCrawlRequestForm()
    
    context['form'] = my_form
    return render(response, "main/create_crawl.html", context)

def create_steps(response):
    
    print('################################3')
    print(response)
    print('################################3')
    print("Estou no create_steps")
    print('################################3')
    
    return render(response, "main/steps_creation.html", {})