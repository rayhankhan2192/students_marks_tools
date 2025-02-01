from .models import Batch, Student, Section, Quiz
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id','batchName']
    def validate(self, data):
        if Batch.objects.filter(
            batchName=data['batchName'],
        ).exists():
            raise serializers.ValidationError(
                "Already exists."
            )
        return data

class SectionCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
    def validate(self, data):
        if Section.objects.filter(
            batch = data['batch'],
            sectionName = data['sectionName'],
        ).exists():
            raise serializers.ValidationError(
                "Already exists."
            )
        return data

class SectionSerializers(serializers.ModelSerializer):
    batch = serializers.CharField(source='batch.batchName', read_only=True)
    class Meta:
        model = Section
        fields = ['batch', 'sectionName']
        
class StudentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
class StudentSerializers(serializers.ModelSerializer):
    section = serializers.CharField(source='section.section_name', read_only=True)
    batch_name = serializers.CharField(source='section.batch_name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['student_id', 'section', 'batch_name']

class QuizCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        
class QuizSerializers(serializers.ModelSerializer):
    section = serializers.CharField(source='section.section_name', read_only=True)
    batch_name = serializers.CharField(source='section.batch', read_only=True)
    class Meta:
        model = Quiz
        fields = ['quiz_name', 'section', 'batch_name', 'course_code']
        
    

