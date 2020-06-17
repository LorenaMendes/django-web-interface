from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_crawlers, name="list_crawlers"),
    path("crawlers/", views.list_crawlers, name="list_crawlers"),
    path("new/", views.create_crawler, name="create_crawler"),
    path("delete/<int:id>/", views.delete_crawler, name="delete_crawler"),
    path("detail/<int:id>/", views.detail_crawler, name="detail_crawler"),
    path("crawlers/steps/", views.create_steps, name="create_steps"),
    path("monitoring/", views.monitoring, name="monitoring"),
    path("detail/manage_crawl/<int:instance_id>", views.manage_crawl, name="manage_crawl"),
]