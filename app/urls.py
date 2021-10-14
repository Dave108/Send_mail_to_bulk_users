from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.csv_read_view, name='homepage'),
]