from django.urls import include, path

urlpatterns = [
    path(r'', include('rest_framework_social_oauth2.urls')),
]
