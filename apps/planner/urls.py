from django.urls import path
from . import views

urlpatterns = [
    path("suggest", views.suggest, name="suggest"),
    path("create", views.create, name="create"),
    path("update", views.update, name="update"),
    path("history", views.get_all, name="get_all")
]