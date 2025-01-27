from .models import Batch, Student, Section, Quiz, QuizResult
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['batch_name', 'course_name', 'course_code']
    def validate(self, data):
        if Batch.objects.filter(
            batch_name=data['batch_name'],
            course_name=data['course_name'],
            course_code=data['course_code']
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
            section_name = data['section_name'],
            batch = data['batch']
        ).exists():
            raise serializers.ValidationError(
                "Already exists."
            )
        return data

class SectionSerializers(serializers.ModelSerializer):
    batch = serializers.CharField(source='batch.batch_name', read_only=True)
    class Meta:
        model = Section
        fields = ['section_name', 'batch']
        
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
        fields = ['quiz_name', 'section', 'batch_name']
        
class QuizResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['student', 'quiz', 'marks']
    

