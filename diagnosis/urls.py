from django.urls import path, include
# from . import views

urlpatterns = [
    # path('', views.test_job_generator, name='index'),
    path('api/', include('diagnosis.api.urls')),
]
