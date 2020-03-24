from django.contrib import admin
from diagnosis.models import Survey, Question, QuestionOption, Answer, Diagnosis

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(Answer)
admin.site.register(Diagnosis)