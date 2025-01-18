# from django.contrib import admin
# from .models import Batch, Section, Student, Quiz, Mark


# class BatchAdmin(admin.ModelAdmin):
#     list_display = (
#         'batch_name',
#     )

# class SectionAdmin(admin.ModelAdmin):
#     list_display = (
#         'section_name',
#         'batch',
#     )

# class QuizAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'section',
#     )

# class StudentAdmin(admin.ModelAdmin):
#     list_display = (
#         'student_id',
#         'section',
#     )

# class MarksAdmin(admin.ModelAdmin):
#     list_display = (
#         'student',
#         'quiz',
#         'marks',
#     )

# admin.site.register(Batch, BatchAdmin)
# admin.site.register(Section, SectionAdmin)
# admin.site.register(Student, StudentAdmin)
# admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Mark, MarksAdmin)

from django.contrib import admin
from .models import Batch, Student


class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'batch_name',
        'section',
        'course_code',
        'course_name',
    )

class StudentAdmin(admin.ModelAdmin):
    list_display  = (
        'student_id',
        'marks',
        'section',
    )
    
admin.site.register(Batch, BatchAdmin)
admin.site.register(Student, StudentAdmin)