
from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:match_id>/info_match/', views.info_match, name='info_match'),
    path('info/', views.info, name='info'),
]
