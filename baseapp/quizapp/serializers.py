from .models import Batch, Student, Section, Quiz, QuizResult
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id','batch_name', 'course_name', 'course_code']
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

class SectionSerializers(serializers.ModelSerializer):
    batch = serializers.SlugRelatedField(
        queryset=Batch.objects.all(), slug_field="batch_name"
    )
    class Meta:
        model = Section
        fields = ['section_name', 'batch']
    def validate(self, data):
        if Section.objects.filter(
            section_name = data['section_name'],
            batch = data['batch']
        ).exists():
            raise serializers.ValidationError(
                "Already exists."
            )
        return data
            

class StudentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
class StudentSerializers(serializers.ModelSerializer):
    #section = BatchSerializers()
    # section = serializers.CharField(source='section.section', read_only = True)
    # batch = serializers.CharField(source='section.batch_name', read_only = True)
    class Meta:
        model = Student
        # fields = ['student_id', 'marks', 'section', 'batch']
        fields = ['student_id', 'section']
        
class QuizSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['quiz_name', 'section']
        
class QuizResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['student', 'quiz', 'marks']
    

