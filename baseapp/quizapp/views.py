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
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        batches = Batch.objects.all()
        serializer = BatchSerializers(batches, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)
    
class SectionApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = SectionCreateSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Save Successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        section = Section.objects.all()
        serializer = SectionSerializers(section, many = True)
        return Response(serializer.data, status =status.HTTP_200_OK)

class StudentFilterView(APIView):
    def post(self, request):
        data = request.data
        student_id = data.get("student_id")
        section_name = data.get("section_name")
        batch_name = data.get("batch_name")

        # Validate required fields
        if not student_id or not section_name or not batch_name:
            return Response(
                {"message": "Fields 'student_id', 'section_name', and 'batch_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            batch = Batch.objects.get(batch_name=batch_name)
        except Batch.DoesNotExist:
            return Response(
                {"message": f"Batch with name '{batch_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            section = Section.objects.get(section_name=section_name, batch=batch)
        except Section.DoesNotExist:
            return Response(
                {
                    "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create a new student in the section
        student_data = {
            "student_id": student_id,
            "section": section.id,
        }

        serializer = StudentCreateSerializers(data=student_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student added successfully."}, status=status.HTTP_201_CREATED
            )
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        batch_name = request.query_params.get('batch_name')  
        section_name = request.query_params.get('section_name') 
        if not batch_name or not section_name:
            return Response(
                {"message": "Both 'batch_name' and 'section_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            batch = Batch.objects.get(batch_name=batch_name)
        except Batch.DoesNotExist:
            return Response(
                {"message": f"Batch with name '{batch_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            section = Section.objects.get(section_name=section_name, batch=batch)
        except Section.DoesNotExist:
            return Response(
                {
                    "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        students = Student.objects.filter(section=section)
        if not students.exists():
            return Response(
                {"message": "No students found in the specified batch and section."},
                status=status.HTTP_404_NOT_FOUND,
            )
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

class QuizApiView(APIView):
    def post(self, request):
        data = request.data
        quiz_name = data.get("quiz_name")
        section_name = data.get("section_name")
        batch_name = data.get("batch_name")
        
        if not quiz_name or not section_name or not batch_name:
            return Response(
                {"message": "Fields 'quiz_name', 'section_name', and 'batch_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            batch = Batch.objects.get(batch_name=batch_name)
        except Batch.DoesNotExist:
            return Response(
                {"message": f"Batch with name '{batch_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            section = Section.objects.get(section_name=section_name, batch=batch)
        except Section.DoesNotExist:
            return Response(
                {
                    "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        quiz_data = {
            'quiz_name': quiz_name,
            'section': section.id
        }
        serializer = QuizCreateSerializers(data = quiz_data)
        if serializer.is_valid():
            serializer.save()
        return Response(
                {"message": "Quiz create successfully."}, status=status.HTTP_201_CREATED
            )
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        batch_name = request.query_params.get('batch_name')  
        section_name = request.query_params.get('section_name') 
        if not batch_name or not section_name:
            return Response(
                {"message": "Both 'batch_name' and 'section_name' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            batch = Batch.objects.get(batch_name=batch_name)
        except Batch.DoesNotExist:
            return Response(
                {"message": f"Batch with name '{batch_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            section = Section.objects.get(section_name=section_name, batch=batch)
        except Section.DoesNotExist:
            return Response(
                {
                    "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        students = Quiz.objects.filter(section=section)
        if not students.exists():
            return Response(
                {"message": "No students found in the specified batch and section."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = QuizSerializers(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuizMarksApiView(APIView):
    def get(self, request):
        batch_name = request.query_params.get('batch_name')  
        section_name = request.query_params.get('section_name')
        quiz_name = request.query_params.get('quiz_name')
        
        if not batch_name or not section_name or not quiz_name:
            return Response(
                {"message": "Both 'batch_name' & 'section_name' & quiz_num are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            batch = Batch.objects.get(batch_name=batch_name)
        except Batch.DoesNotExist:
            return Response(
                {"message": f"Batch with name '{batch_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            section = Section.objects.get(section_name=section_name, batch=batch)
        except Section.DoesNotExist:
            return Response(
                {
                    "message": f"Section with name '{section_name}' does not exist in batch '{batch_name}'."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            quiz = Quiz.objects.get(quiz_name=quiz_name, section=section)
        except Quiz.DoesNotExist:
            return Response(
                {"message": f"Quiz with name '{quiz_name}' does not exist in section '{section_name}'."},
                status=status.HTTP_404_NOT_FOUND,
            )
        quiz_results = QuizResult.objects.filter(quiz=quiz)
        if not quiz_results.exists():
            return Response(
                {"message": f"No quiz results found for quiz '{quiz_name}' in section '{section_name}'."},
                status=status.HTTP_404_NOT_FOUND,
            )
        results_data = [
            {
                "student_id": result.student.student_id,
                "marks": result.marks
            }
            for result in quiz_results
        ]
        return Response(results_data, status=status.HTTP_200_OK)
        