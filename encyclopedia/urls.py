from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.load_content, name="load_content"),
    path("search", views.search, name="search")
]
