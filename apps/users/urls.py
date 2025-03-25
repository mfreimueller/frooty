from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.authenticate, name='login'), # TODO: move to auth
    path('logout', views.logout, name='logout'),
    path('password', views.update_password, name='update_password')
]