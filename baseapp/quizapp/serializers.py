from .models import Batch, Student
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'batch_name', 'section', 'course_name', 'course_code']
    
class StudentSerializers(serializers.ModelSerializer):
    #section = BatchSerializers()
    section = serializers.CharField(source='section.section', read_only = True)
    batch = serializers.CharField(source='section.batch_name', read_only = True)
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'marks', 'section', 'batch']

