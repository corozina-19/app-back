"""corozina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from auth.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{settings.CURRENT_API_VERSION}/auth/', include('rest_framework.urls')),
    path(f'api/{settings.CURRENT_API_VERSION}/', include('diagnosis.urls')),
    path(f'api/{settings.CURRENT_API_VERSION}/chat/', include('chat.urls')),
    path(f'api/{settings.CURRENT_API_VERSION}/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{settings.CURRENT_API_VERSION}/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    except:
        pass