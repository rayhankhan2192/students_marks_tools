from django.contrib import admin
from .models import Batch, Student, Quiz, QuizResult, Section


# class BatchAdmin(admin.ModelAdmin):
#     list_display = (
#         'batch_name',
#         'section',
#         'course_code',
#         'course_name',
#     )

# class StudentAdmin(admin.ModelAdmin):
#     list_display  = (
#         'student_id',
#         'marks',
#         'section',
#     )
    
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Section)