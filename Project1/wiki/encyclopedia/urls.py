from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.entry_display, name="wiki"),
    # path("<str:title>", views.entries, name="django"),
    # path("git", views.entries, name="git"),    
    # path("html", views.entries, name="html"),
    # path("python", views.entries, name="python"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage")
]
