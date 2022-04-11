from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("wiki/<str:title>/", views.load_content, name="load_content"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("random", views.random_page, name="random"),
    path("edit/<str:title>/", views.edit, name="edit")
]
