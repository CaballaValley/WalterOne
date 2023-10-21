
from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:match_id>/info_match/', views.info_match, name='info_match'),
    path('info/', views.info, name='info'),
    path('graph/<int:match_id>', views.graph, name='graph'),
    path('graph_data/<int:match_id>', views.match_data, name='graph-data'),
]
