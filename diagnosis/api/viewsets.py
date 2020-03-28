from rest_framework import viewsets, permissions
from diagnosis import models
from diagnosis.api import serializers


class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = serializers.SurveySerializer
    queryset = models.Survey.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['read_only'] = self.action in ('retrieve', 'detail')
        return context


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['question_creation'] = True
        return context


class QuestionOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = serializers.QuestionOptionSerializer
    queryset = models.QuestionOption.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['questionoption_creation'] = True
        return context
