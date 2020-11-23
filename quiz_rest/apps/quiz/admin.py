from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import *
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_start', 'date_end', 'descript', 'is_active']
    inlines = [QuestionInline]

    class Meta:
        model = Quiz

class AnswerBooleanInline(admin.TabularInline):
    model = AnswerBoolean
    extra = 0

class AnswerTextInline(admin.TabularInline):
    model = AnswerText
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'type_questions']
    inlines = [AnswerBooleanInline, AnswerTextInline]

    class Meta:
        model = Question

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerText)
admin.site.register(AnswerBoolean)

admin.site.register(Post_user)
admin.site.register(Result)