from django.contrib import admin
from .models import Batch, Section, Student, Quizs, Marks


class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'batch_name',
    )

class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'section_name',
        'batch',
    )

class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'section',
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'section',
    )

class MarksAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'quiz',
        'marks',
    )

admin.site.register(Batch, BatchAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Quizs, QuizAdmin)
admin.site.register(Marks, MarksAdmin)