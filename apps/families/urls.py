from django.urls import path
from . import views

urlpatterns = [
    path('', views.FamilyListCreateView.as_view(), name='families-cr'),
    path('<int:meal_id>', views.FamilyUpdateDeleteView.as_view(), name='family-ud'),
    path('<int:meal_id>/<str:user_name>', views.FamilyUserModifyView.as_view(), name='family-user'),
]