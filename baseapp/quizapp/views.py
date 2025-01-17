from django.shortcuts import render
from .serializers import BatchSerializers
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