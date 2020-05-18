from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("crawlers/", views.crawlers, name="crawlers"),
    path("monitoring/", views.monitoring, name="monitoring"),
]