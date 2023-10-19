from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers


from api.admin import admin_site
from api.views.actions import AttackViewSet, DefendViewSet,  MoveViewSet
from api.views.matches import FindViewSet
from utils.static import static
from web import urls as web_urls


router = routers.DefaultRouter()
router.register(r'attacks', AttackViewSet)
router.register(r'defends', DefendViewSet, basename='defend')
router.register(r'moves', MoveViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('admin-match-panel/', admin_site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('finds/', FindViewSet.as_view({'get': 'retrieve'})),
    path('web/', include(web_urls.urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
