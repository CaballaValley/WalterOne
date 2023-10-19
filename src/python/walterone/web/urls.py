
from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:match_id>/zones/', views.zones, name='zones_match'),
    path('info/', views.info, name='info'),
]
