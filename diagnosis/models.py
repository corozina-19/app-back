from django.db import models
from django.contrib.auth.models import User
from diagnosis.constants import QUESTION_TYPE, YES_NO_QUESTION


class Survey(models.Model):
    name = models.CharField(max_length=50)
    percentage_acceptance = models.FloatField(default=0)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    type = models.IntegerField(choices=QUESTION_TYPE, default=YES_NO_QUESTION)
    statement = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f'Survey {self.survey}: {self.statement}'


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    value = models.IntegerField(default=0)
    text = models.CharField(max_length=150)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f'Question: {self.question.statement}: {self.text} ({self.value})'


class Diagnosis(models.Model):
    patient = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    score_percentage = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Diagnoses"

    def __str__(self):
        return f'Survey: {self.survey.name} => Patient: {self.patient.get_full_name()}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    answer_value = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        value = self.answer_value
        return f'Diagnosis: {self.diagnosis} Question: {self.question.survey} Answer: {self.answer_text} ({value})'
