from .models import Batch, Student
from rest_framework import serializers


class BatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

    
class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

