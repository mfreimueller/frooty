from django.urls import path
from . import views

urlpatterns = [
    path('', views.HistoryListCreateView.as_view(), name='history-cr'),
    path('<int:meal_id>', views.HistoryUpdateDeleteView.as_view(), name='history-ud')
]