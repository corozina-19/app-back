from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()
router.register('survey', viewsets.SurveyViewSet,)
router.register('question', viewsets.QuestionViewSet,)
router.register('question-option', viewsets.QuestionOptionViewSet,)

urlpatterns = [
    path('', include(router.urls)),
]
