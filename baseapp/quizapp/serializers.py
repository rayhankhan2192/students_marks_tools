from .models import Batch, Student, Section, Quiz, Subject
from rest_framework import serializers
from rest_framework.response import Response
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
    #section_info = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id','batch', 'section', 'subjectName', 'subjectCode']
    def validate_batch(self, value):
        """Ensure that the batch belongs to the authenticated user, that the subject
        does not already exist for the batch and section, and that the section exists for the batch."""
        request = self.context.get('request')
        user = request.user

        # Check if the batch belongs to the authenticated user
        if not Section.objects.filter(id=value.id, auth_users=user).exists():
            raise serializers.ValidationError("You can only add Subject for section and batches you own.")
        
        # Check if the section belongs to the given batch
        section = self.initial_data.get('section')  # Get the section from the request data
        if not Section.objects.filter(batch=value, id=section).exists():
            raise serializers.ValidationError("This section does not exist for the selected batch.")

        # Check if a subject already exists for the given section and batch
        if Subject.objects.filter(batch=value, section_id=section).exists():
            raise serializers.ValidationError("A subject already exists for this batch and section.")

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
            batch = validated_data['batch'],
            auth_users = user
            
        ).exists():
            raise serializers.ValidationError({"message": "Already exists for this user."})
        validated_data['auth_users'] = user
        return super().create(validated_data)
    
    # def get_section_info(self, obj):
    #     if obj.section:
    #         return f"{obj.section.sectionName}-{obj.section.batch}"
    #     return None
        
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


        
class QuizSerializers(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset = Student.objects.all(), write_only = True)
    subject = serializers.PrimaryKeyRelatedField(queryset = Subject.objects.all(), write_only = True)
    class Meta:
        model = Quiz
        fields = ['id', 'student', 'subject', 'marks', 'quizNo']
        
    def validate_student(self, value):
        request = self.context.get('request')
        user = request.user
        if not Student.objects.filter(id=value.id, auth_users=user).exists():
            raise serializers.ValidationError("You can only add Student you own.")
        return value
    
    def validate_subject(self, value):
        request = self.context.get('request')
        user = request.user
        if not Subject.objects.filter(id=value.id, auth_users = user).exists():
            raise serializers.ValidationError("You can only add Subject for Student you own.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        user = request.user
        if Quiz.objects.filter(
            student = validated_data['student'],
            subject = validated_data['subject'],
            # marks = validated_data['marks'],
            quizNo = validated_data['quizNo'],
            auth_users = user
        ).exists():
            raise serializers.ValidationError({"message": "Already exists for this user."})
        validated_data['auth_users'] = user
        return super().create(validated_data)

class QuizGetSerializers(serializers.ModelSerializer):
    batch = serializers.CharField(source = 'student.section.batch.batchName')
    section = serializers.CharField(source = 'student.section.sectionName',  read_only=True)
    subject = serializers.CharField(source = 'subject.subjectName')
    class Meta:
        model = Quiz
        fields = ['quizNo','batch', 'section', 'subject','student', 'marks']

# class SectionGetSerilizers(serializers.ModelSerializer):
#     batch = serializers.CharField(source = 'batch.batchName')
#     class Meta:
#         model = Section
#         fields = ['sectionName', 'batch']