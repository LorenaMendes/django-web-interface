from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_crawlers, name="list_crawlers"),
    path("crawlers/", views.list_crawlers, name="list_crawlers"),
    path("create_crawler/", views.create_crawler, name="create_crawler"),
    path("crawlers/steps/", views.create_steps, name="create_steps"),
    path("monitoring/", views.monitoring, name="monitoring"),
    path("crawlers/manage_crawl/<int:instance_id>", views.manage_crawl, name="manage_crawl"),
]