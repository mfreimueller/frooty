from django.urls import path
from . import views

urlpatterns = [
    path("", views.SuggestView.as_view(), name="suggest")
]