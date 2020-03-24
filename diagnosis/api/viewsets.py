from rest_framework import viewsets
from diagnosis import models
from diagnosis.api import serializers


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SurveySerializer
    queryset = models.Survey.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['survey_creation'] = True
        return context


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['question_creation'] = True
        return context


class QuestionOptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionOptionSerializer
    queryset = models.QuestionOption.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['questionoption_creation'] = True
        return context
