"""walterone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers


from api.admin import admin_site
from api.views.actions import AttackViewSet, DefendViewSet,  MoveViewSet
from api.views.matches import FindViewSet


router = routers.DefaultRouter()
router.register(r'attacks', AttackViewSet)
router.register(r'defends', DefendViewSet, basename='defend')
router.register(r'moves', MoveViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('admin-match-panel/', admin_site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('finds/', FindViewSet.as_view({'get': 'retrieve'}))
]
