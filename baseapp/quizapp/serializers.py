from .models import Batch, Student
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'batch_name', 'section', 'course_name', 'course_code']
    
class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'marks', 'section']

