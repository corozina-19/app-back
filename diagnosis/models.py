from django.db import models
from django.contrib.auth.models import User
from diagnosis.constants import QUESTION_TYPE, YES_NO_QUESTION


class Survey(models.Model):
    name = models.CharField(max_length=50)
    percentage_acceptance = models.FloatField(default=0)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def calculate_total_score(self):
        total_score = 0
        questions = self.questions.all().prefetch_related('options')
        for question in questions:
            total_score += max(question.options.all().values_list('value', flat=True))

        self.total_score = total_score
        self.save()


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Only on saving a new Question option for a survey question the total score can change.
        """
        super(QuestionOption, self).save(force_insert, force_update, using, update_fields)

        self.question.survey.calculate_total_score()


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
