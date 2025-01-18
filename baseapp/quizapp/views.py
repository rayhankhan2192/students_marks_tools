from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework import status


class BatchApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = BatchSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        batches = Batch.objects.all()
        serializer = BatchSerializers(batches, many = True)
        return Response(serializer.data)


class StudentFilterView(APIView):
    def post(self, request):
        data = request.data
        serializer = StudentCreateSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        batch_name = request.query_params.get('batch_name')  
        section_name = request.query_params.get('section') 
        students = Student.objects.all()

        if batch_name and section_name:
            students = students.filter(section__batch_name=batch_name, section__section=section_name)
            if not students.exists():
                return Response({'message': 'No students found!'}, status=status.HTTP_404_NOT_FOUND)
        elif batch_name:
            students = students.filter(section__batch_name=batch_name)
            if not students.exists():
                return Response({'message': 'No students found!'}, status=status.HTTP_404_NOT_FOUND)
        elif section_name:
            students = students.filter(section__section=section_name)
            if not students.exists():
                return Response({'message': 'No students found!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StudentSerializers(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, *args, **kwargs):
        batch_name = request.query_params.get('batch_name')  
        section_name = request.query_params.get('section') 

        if not batch_name or not section_name:
            return Response({'message': 'Batch name and section are required for updating.'}, status=status.HTTP_400_BAD_REQUEST)

        student_id = request.data.get('student_id')  
        if not student_id:
            return Response({'message': 'Student ID is required for updating.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(
                section__batch_name=batch_name,
                section__section=section_name,
                student_id=student_id
            )
        except Student.DoesNotExist:
            return Response({'message': 'No student found with the given criteria.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializers(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student updated successfully!', 'student': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_id, *args, **kwargs):
        try:
            student = Student.objects.get(student_id=student_id)
            student.delete()
            return Response({'message': 'Student deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({'message': 'Student not found!'}, status=status.HTTP_404_NOT_FOUND)