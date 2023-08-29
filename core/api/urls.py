from django.conf.urls import url
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from core.api.views import UserViewSet, UserTransactionViewSet

urlpatterns = []

router = routers.DefaultRouter(trailing_slash=True)
router.register('users', UserViewSet, basename='users')
router.register('user_transactions', UserTransactionViewSet, basename='user_transactions')

urlpatterns += router.urls

schema_view = get_schema_view(
    openapi.Info(
        title="Public API",
        default_version='v1',
    ),
    patterns=[path('api/v1/', include('core.api.urls')), ],
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json', ),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui', ),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc', ),
]
