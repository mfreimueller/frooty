from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterUserView.as_view(), name='register-user'),
    path('', views.ManageUserView.as_view(), name='manage-users')
]