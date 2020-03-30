from rest_framework import viewsets, permissions
from rest_framework.status import HTTP_201_CREATED

from diagnosis.models import Survey
from diagnosis.api import serializers
from diagnosis.models import Diagnosis, Question, QuestionOption
from diagnosis.utils import calculate_percentage


class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = serializers.SurveySerializer
    queryset = Survey.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['read_only'] = self.action in ('retrieve', 'detail')
        return context


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['question_creation'] = True
        return context


class QuestionOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly, ]
    serializer_class = serializers.QuestionOptionSerializer
    queryset = QuestionOption.objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['questionoption_creation'] = True
        return context


class DiagnosisViewset(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()

    def get_serializer_class(self):

        if self.action in ['retrieve', 'list']:
            return serializers.DiagnosisScoredSerializer

        return serializers.DiagnosisSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Intercepts response and calculate diagnosis results
        """
        if response.status_code == HTTP_201_CREATED:
            diagnosis = Diagnosis.objects.get(pk=response.data.get('id'))
            serializer = calculate_percentage(diagnosis)
            response.data['score'] = serializer.data
        return super(DiagnosisViewset, self).finalize_response(request, response, *args, **kwargs)
