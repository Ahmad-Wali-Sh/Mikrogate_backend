"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from taskmanager.views import create_notification_all, create_notification_noc,create_notification_users, create_notification_tech,create_notification_l1, create_notification_sales

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/taskmanager/', include('taskmanager.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/notification_create_all', create_notification_all, name='create_notification_all'),
    path('api/notification_create_noc', create_notification_noc, name='create_notification_noc'),
    path('api/notification_create_tech', create_notification_tech, name='create_notification_tech'),
    path('api/notification_create_l1', create_notification_l1, name='create_notification_l1'),
    path('api/notification_create_sales', create_notification_sales, name='create_notification_sales'),
    path('api/notification_create_users', create_notification_users, name='create_notification_users'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
