"""kryptonite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .router import router


schema_view = get_schema_view(
    openapi.Info(
        title="Krypto API",
        default_version='v1',
        description="Krypto application django API",
        #terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ouko.sherman@gmail.com"),
        #license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((router.urls, 'customusers'))),
    path('', include((router.urls, 'regions'))),
    path('', include((router.urls, 'agents'))),
    path('', include((router.urls, 'branches'))),
    path('', include((router.urls, 'landlords'))),
    path('', include((router.urls, 'caretakers'))),
    path('', include((router.urls, 'apartments'))),


    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
