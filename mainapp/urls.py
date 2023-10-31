from . import views
from django.urls import path

app_name = "mainapp"
urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("pl/", views.home_view_pl, name="home_view_pl"),
    path("new/", views.new_article_view, name="new_article"),
    path("<int:article_id>/", views.article_view, name="article_view"),
    path("<str:article_url>/", views.article_view_url, name="article_view_url"),
    path("edit/<int:article_id>/", views.edit_article_view, name="edit_article"),
    path("delete/<int:article_id>/", views.delete_article_view, name="delete_article"),
    path("access_denied/", views.access_denied_view, name="access_denied"),
]

