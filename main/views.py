from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CrawlRequestForm, RawCrawlRequestForm
from .models import CrawlRequest, CrawlerInstance

import crawlers.crawler_manager as crawler_manager

def getAllData():
    return CrawlRequest.objects.all().order_by('-creation_date')

def list_crawlers(response):
    context = {'allcrawlers': getAllData()}
    return render(response, "main/list_crawlers.html", context)


def create_crawler(response):
    context = {}
    if response.method == "POST":
        my_form = RawCrawlRequestForm(response.POST)
        if my_form.is_valid():
            new_crawl = CrawlRequestForm(my_form.cleaned_data)
            print("************")
            print(new_crawl)
            print("************")
            new_crawl.save()
            
            return HttpResponseRedirect('http://localhost:8000/crawlers/')
            # return render(response, "main/list_crawlers.html", context)
    else:
        my_form = RawCrawlRequestForm()
    context['form'] = my_form
    return render(response, "main/create_crawler.html", context)

def delete_crawler(request, id):
    crawler = CrawlRequest.objects.get(id=id)
    print("OI1")
    
    if request.method == 'POST':
        print("OI2")
        crawler.delete()
        return HttpResponseRedirect('http://localhost:8000/crawlers/')
    
    return render(request, 'main/confirm_delete_modal.html', {'crawler': crawler})

def detail_crawler(request, id):
    crawler = CrawlRequest.objects.get(id=id)
    
    # if request.method == 'POST':
        
    #     return HttpResponseRedirect('http://localhost:8000/crawlers/')
    
    return render(request, 'main/detail_crawler.html', {'crawler': crawler})

def monitoring(response):
    return HttpResponseRedirect("http://localhost:5000/")

def create_steps(response):
    return render(response, "main/steps_creation.html", {})

def manage_crawl(response, instance_id):
    data = CrawlRequest.objects.filter(id=instance_id).values()[0]
    full_data = CrawlRequest.objects.filter(id=instance_id).values()[0]
    del data['creation_date']
    del data['last_modified']
    instance_id = crawler_manager.start_crawler(data)
    
    obj = create_instance(data['id'], instance_id)
    context = {'obj':obj, 'crawler':full_data}
    return render(response, "main/detail_crawler.html", context)

def create_instance(crawler_id, instance_id):
    mother = CrawlRequest.objects.filter(id=crawler_id)
    obj = CrawlerInstance.objects.create(crawler_id=mother[0], instance_id=instance_id, running=True)
    return obj
