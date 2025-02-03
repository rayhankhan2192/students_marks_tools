from .models import Batch, Student, Section, Quiz, Subject
from rest_framework import serializers


# class BatchSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Batch
#         fields = ['id','batchName']
#     def validate(self, data):
#         if Batch.objects.filter(
#             batchName=data['batchName'],
#         ).exists():
#             raise serializers.ValidationError(
#                 "Already exists."
#             )
#         return data
    
#     def create(self, validated_data):
#         validated_data['auth_users'] = self.context['request'].user
#         return super().create(validated_data)

class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'batchName'] 

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        user = request.user
        if Batch.objects.filter(batchName=validated_data['batchName'], auth_users=user).exists():
            raise serializers.ValidationError({"message": "This batch name already exists for this user."})
        validated_data['auth_users'] = user  # Assign authenticated user
        return super().create(validated_data)

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
        fields = ['id','batch', 'sectionName']
        
class SubjectSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        
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
        
    

