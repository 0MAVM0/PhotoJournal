from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="PhotoJournal API",
        default_version='v1',
        description="PhotoJournal is mini app which is similar with Instagram",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[ AllowAny ],
)

urlpatterns = [
    # Documentation Of API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Django core and other applications
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/follows/', include('posts.urls')),
    path('api/chats/', include('chats.urls')),
    path('', include('web_grok.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
