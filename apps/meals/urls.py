from django.urls import path
from . import views

urlpatterns = [
    path('', views.MealListCreateView.as_view(), name='meals-cr'),
    path('<int:meal_id>', views.MealUpdateDeleteView.as_view(), name='meal-ud')
]