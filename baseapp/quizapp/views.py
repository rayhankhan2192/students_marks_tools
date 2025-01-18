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
        serializer = StudentSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        batch_name = request.query_params.get('batch_name')  # Get batch_id from query params
        section_name = request.query_params.get('section')  # Get section name from query params

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