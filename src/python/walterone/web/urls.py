
from django.urls import path

from . import views

urlpatterns = [
    path('<int:match_id>/info_match/', views.info_match, name='info_match'),
    path('<int:match_id>/info_match_zones/', views.info_match_zones, name='info_match_zones'),
    path('info/', views.info, name='info'),
]
