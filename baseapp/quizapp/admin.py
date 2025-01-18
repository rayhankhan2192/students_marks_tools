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