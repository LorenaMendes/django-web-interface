from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("crawlers/", views.create_crawl, name="create_crawl"),
    path("monitoring/", views.monitoring, name="monitoring"),
]