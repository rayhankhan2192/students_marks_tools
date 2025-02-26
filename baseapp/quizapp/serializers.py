from .models import Batch, Student, Section, Quiz, Subject
from rest_framework import serializers

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

class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id','batch', 'sectionName']
        
    def validate_batch(self, value):
        """Ensure that the batch belongs to the authenticated user."""
        request = self.context.get('request')
        user = request.user
        if not Batch.objects.filter(id=value.id, auth_users=user).exists():
            raise serializers.ValidationError("You can only create a section for batches you own.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        user = request.user
        
        if Section.objects.filter(sectionName = validated_data['sectionName'], batch=validated_data['batch'], auth_users = user).exists():
             raise serializers.ValidationError({"message": "This Section & Batch name already exists for this user."})
        validated_data['auth_users'] = user
        return super().create(validated_data)

        
class SubjectSerialisers(serializers.ModelSerializer):
    """Makes section writable and available in validated_data.
    Only accepts section IDs from requests."""
    section = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), write_only=True
    ) 
    section_info = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'section', 'subjectName', 'subjectCode', 'section_info']
    def validate_batch(self, value):
        """Ensure that the batch belongs to the authenticated user."""
        request = self.context.get('request')
        user = request.user
        if not Section.objects.filter(id=value.id, auth_users=user).exists():
            raise serializers.ValidationError("You can only add Subject for section and batches you own.")
        return value
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        user = request.user
        if Subject.objects.filter(
            section = validated_data['section'],
            subjectName = validated_data['subjectName'],
            subjectCode = validated_data['subjectCode'],
            auth_users = user
            
        ).exists():
            raise serializers.ValidationError({"message": "Already exists for this user."})
        validated_data['auth_users'] = user
        return super().create(validated_data)
    
    def get_section_info(self, obj):
        if obj.section:
            return f"{obj.section.sectionName}-{obj.section.batch}"
        return None
        
class StudentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
class StudentSerializers(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), write_only = True
    )
    section_info = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['id', 'studentId', 'section', 'section_info']
        
    def validate_section(self, value):
        request = self.context.get('request')
        user = request.user
        if not Section.objects.filter(id=value.id, auth_users=user).exists():
            raise serializers.ValidationError("You can only add Subject for section and batches you own.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        user = request.user
        if Student.objects.filter(
            studentId = validated_data['studentId'],
            section = validated_data['section'],
            auth_users = user
        ).exists():
            raise serializers.ValidationError({"message": "Already exists for this user."})
        validated_data['auth_users'] = user
        return super().create(validated_data)
    
    def get_section_info(self, obj):
        if obj.section:
            return f"{obj.section.sectionName}-{obj.section.batch}"
        return None
        

# class StudentSerializers(serializers.ModelSerializer):
#     section = serializers.CharField(source='section.section_name', read_only=True)
#     batch_name = serializers.CharField(source='section.batch_name', read_only=True)
    
#     class Meta:
#         model = Student
#         fields = ['student_id', 'section', 'batch_name']

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
        
    

