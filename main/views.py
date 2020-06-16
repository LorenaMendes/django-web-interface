from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CrawlRequestForm, RawCrawlRequestForm
from .models import CrawlRequest
# from .src.crawler_manager import start_crawler

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
            new_crawl.save()
            
            return HttpResponseRedirect('http://localhost:8000/crawlers/')
            # return render(response, "main/list_crawlers.html", context)
    else:
        my_form = RawCrawlRequestForm()
    context['form'] = my_form
    return render(response, "main/create_crawler.html", context)

def delete_crawler(request, id):
    crawler = CrawlRequest.objects.get(id=id)
    
    if request.method == 'POST':
        crawler.delete()
        return HttpResponseRedirect('http://localhost:8000/crawlers/')
    
    return render(request, 'main/confirm_delete_modal.html', {'crawler': crawler})

def detail_crawler(request, id):
    crawler = CrawlRequest.objects.get(id=id)
    print("***************")
    print(crawler)
    
    # if request.method == 'POST':
        
    #     return HttpResponseRedirect('http://localhost:8000/crawlers/')
    
    return render(request, 'main/detail_crawler.html', {'crawler': crawler})

def monitoring(response):
    return HttpResponseRedirect("http://localhost:5000/")

def create_steps(response):
    return render(response, "main/steps_creation.html", {})

def manage_crawl(response, instance_id):
    
    # data = CrawlRequest.objects.filter(id=instance_id).values()[0]
    # del data['creation_date']
    # del data['last_modified']

    # command, instance_id = start_crawler(data)

    # print("*******************")
    # print(command)
    # print("*******************")
    return render(response, "main/list_crawlers.html", {})