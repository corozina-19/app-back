from django.db import models
from django.contrib.auth.models import User
from diagnosis.constants import QUESTION_TYPE, YES_NO_QUESTION


class Survey(models.Model):
    name = models.CharField(max_length=50)
    percentage_acceptance = models.FloatField(default=0)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    type = models.IntegerField(choices=QUESTION_TYPE, default=YES_NO_QUESTION)


class QuestionOptions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    text = models.CharField(max_length=150)


class Diagnosis(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    score_percentage = models.FloatField(default=0)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    answer_text = models.TextField()
    answer_value = models.IntegerField()
