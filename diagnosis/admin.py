from django.contrib import admin
from diagnosis.models import Survey, Question, QuestionOption, Answer, Diagnosis

# Register your models here.

admin.site.register(Survey)


class QuestionOptionTabularInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = (QuestionOptionTabularInline, )


admin.site.register(Question, QuestionAdmin)

admin.site.register(QuestionOption)
admin.site.register(Answer)
admin.site.register(Diagnosis)
