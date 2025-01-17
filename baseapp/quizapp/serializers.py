from .models import *
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        models = Section
        fields = '__all__'

class QuizSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
    
class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class MarkSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'
